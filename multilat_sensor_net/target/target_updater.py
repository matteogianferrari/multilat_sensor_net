"""This module implements the TargetUpdater class.

The TargetUpdater class manages updating a target's position in a 3D space based on predefined
trajectory waypoints loaded from a JSON file. The position updates are performed in a
separate thread at a specified frequency, with an option to loop the trajectory indefinitely.

Classes:
    TargetUpdater: TargetService class for managing target position updates in 3D space.

Usage Example:
    from tri_sensor_net.target import TargetUpdater, TargetObject
    import time
    import numpy as np

    obj = TargetObject(start_pos=np.array([0., 0., 0.]))
    updater = TargetUpdater(target_ref=obj, path_file="path.json", freq=40, loop_path=True)
    updater.start()

    time.sleep(5)
"""

import numpy as np
import threading as th
import time
import json


class TargetUpdater:
    """TargetUpdater class for managing target position updates in 3D space.

    This class handles updating the position of a target object based on a
    sequence of waypoints defined in a JSON file. It operates in a separate daemon thread,
    updating the target's position at a specified frequency.
    The updater can loop the trajectory indefinitely if desired.

    Attributes:
        target_ref: A `TargetObject` reference representing the domain logic for managing
            the target's position in a 3D space.
        path_file: A string containing the path to the JSON file that holds the trajectory waypoints.
        freq: A float indicating the target position updating frequency [Hz].
        loop_path: A bool indicating whether to repeat in loop the trajectory.
        waypoints: A list containing the trajectory waypoints that the target must follow
            (e.g. of waypoint, { "x": 5.0000, "y": 2.5000, "z": 1.2 }).
        _thread: A threading daemon thread where the target position is updated based
            on the trajectory waypoints at the specified frequency.
    """

    def __init__(self, target_ref, path_file: str, freq: float, loop_path: bool) -> None:
        """Initializes the TargetUpdater.

        Args:
            target_ref: A `TargetObject` reference for handling domain logic.
            path_file: The JSON file path containing the trajectory.
            freq: The update frequency [Hz] for the thread.
            loop_path: Flag indicating whether to loop the waypoints.

        Raises:
            ValueError: If the JSON file doesn't contain any waypoints (it's empty).
        """
        self.target_ref = target_ref

        # Trajectory attributes
        self.path_file = path_file
        self.freq = freq
        self.loop_path = loop_path

        self.waypoints = self._read_waypoints()
        if not self.waypoints:
            raise ValueError("TargetUpdater: No waypoints found in the specified JSON file.")

        # The daemon thread is used to avoid the necessity of joining it to the main thread.
        # When the main thread finished its work, the daemon thread will be automatically stopped,
        # avoiding the requirement of a stop function and signal.
        self._thread = th.Thread(target=self._run, daemon=True)

    def _read_waypoints(self) -> list:
        """Reads the waypoints from the specified JSON file.

        Returns:
            The list of waypoints extracted from the JSON file.

        Raises:
            ValueError: If a waypoint doesn't contain X, Y, Z coordinates.
            ValueError: If the waypoint format is different from the specified standard.
        """
        # Reads the data from the JSON file
        with open(self.path_file, 'r') as f:
            data = json.load(f)

        waypoints = []

        # Loops to extract each single waypoint
        for entry in data:
            if isinstance(entry, dict):
                # Format: {"x": val, "y": val, "z": val}
                if "x" in entry and "y" in entry and "z" in entry:
                    x, y, z = entry["x"], entry["y"], entry["z"]
                    waypoints.append(np.array([x, y, z]))
                else:
                    raise ValueError(f"TargetUpdater: Invalid waypoint object. Must contain x, y, z keys: {entry}")
            else:
                raise ValueError(f"TargetUpdater: Invalid waypoint format: {entry}")

        return waypoints

    def _run(self) -> None:
        """Thread body function that updates the target position.

        The target position is updated following the trajectory specified by the waypoints.
        When 'loop_path' is set to True, the function will continue to execute until the main thread is running.
        When 'loop_path' is set to False, the function will terminate after completing the trajectory once.
        """
        index = 0

        # Computes the time interval
        interval = 1.0 / self.freq

        print("TargetUpdater: Thread started, following path from JSON file.")

        # Update loop
        while True:
            current_waypoint = self.waypoints[index]
            self.target_ref.set_position(new_pos=current_waypoint)
            print(f"TargetUpdater: Updated the position to: {current_waypoint[0]:.3f};{current_waypoint[1]:.3f};{current_waypoint[2]:.3f}")

            # Sleeps to meet the required frequency
            time.sleep(interval)

            index += 1

            # Loop path logic
            if index >= len(self.waypoints):
                if self.loop_path:
                    index = 0  # restart the path from the beginning
                else:
                    break

        print("TargetUpdater: Thread stopped.")

    def start(self) -> None:
        """Starts the thread for updating the target position.
        """
        self._thread.start()
