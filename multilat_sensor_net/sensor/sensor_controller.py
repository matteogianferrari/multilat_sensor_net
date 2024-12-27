"""This module implements the SensorController class.

The SensorController class serves as a facade for managing a distance sensor in a 3D space.
It coordinates the creation of the SensorData and SensorUpdater classes,
providing a simplified interface to measure the distance from the sensor to a target
at a specified frequency.

Classes:
    SensorController: SensorController serves as a facade for managing a distance sensor in a 3D space.

Usage Example:
    from multilat_sensor_net.sensor import SensorController
    import numpy as np

    obj = SensorController(node_id=1, pos=np.array([0., 0., 0.]), service_addr="localhost:50051", verbose=False)
    obj.start()

    time.sleep(1)
    obj.get_distance()  # Output: 5.634
    time.sleep(5)
"""

from multilat_sensor_net.sensor import SensorData, SensorUpdater
import numpy as np


class SensorController:
    """SensorController serves as a facade for managing a distance sensor in a 3D space.

    This class encapsulates the creation and coordination of the SensorData, and SensorUpdater
    classes. It provides a simplified interface to start and manage the sensor's behavior, including
    updating the Euclidean distance between the sensor and the target's position at a specified frequency.

    Attributes:
        data: A SensorData instance that encapsulates the sensor's state.
        updater: A SensorUpdater instance responsible for updating the Euclidean distance between the
            sensor and the target's position. It operates in a separate thread at a specified frequency.
    """

    def __init__(
            self,
            node_id: int,
            pos: np.array,
            service_addr: str,
            acc: float = 0.003,
            freq: float = 40,
            verbose: bool = False
    ) -> None:
        """Initializes the SensorController.

        Args:
            node_id: The ID related to the node that possesses the distance sensor.
            pos: A 3D numpy array containing the position of the distance sensor.
            service_addr: The socket address (e.g., "localhost:50051") where the gRPC server is
                listening for incoming connections.
            acc: The accuracy for the random Uniform noise added to the measured distance [m].
            freq: The frequency [Hz] at which distance measurements are taken.
            verbose: Flag indicating whether the classes must produce an output.
        """
        # Domain object
        self.data = SensorData()

        # Measuring thread
        self.updater = SensorUpdater(
            data_ref=self.data,
            node_id=node_id,
            pos=pos,
            service_addr=service_addr,
            acc=acc,
            freq=freq,
            verbose=verbose
        )

    def start(self) -> None:
        """Starts the sensor controller's measurement loop.

        This method initiates the distance updater thread, which continuously obtains the target's
        position via gRPC, computes the distance (with Gaussian noise), and updates the sensor's
        domain object. The loop runs until the main application ends or a gRPC error occurs.
        """
        self.updater.start()

    def get_distance(self) -> float:
        """Retrieves the last measured distance between the sensor and the target.

        Returns:
            A float indicating the most recent distance measurement in meters.
        """
        return self.data.get_distance()
