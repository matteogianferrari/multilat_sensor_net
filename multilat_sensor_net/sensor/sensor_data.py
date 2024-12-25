"""This module implements the SensorData class.

The SensorData class is used for representing a distance sensor into 3D Euclidean space.

Classes:
    SensorData: SensorData class for managing a thread-safe distance sensor in a 3D space.

Usage Example:
    import numpy as np
    from multilat_sensor_net.sensor import SensorData

    obj = SensorData()
    obj.set_distance(new_distance=4.7)

    obj.get_distance()  # Output: 4.7
"""

import threading as th
import numpy as np


class SensorData:
    """SensorData class for managing a thread-safe distance sensor in a 3D space.

    This class represents a distance sensor placed in a 3D Euclidean space. This class provides methods for
    setting and retrieving the current measured distance between the sensor and the target.

    This class is thread-safe and provides methods that allow avoiding starvation and deadlock.

    Attributes:
        _distance: A float indicating the Euclidean distance in meters [m] between the sensor and the target.
        _mutex: A threading mutex used to lock critical sections of the code.
    """

    def __init__(self) -> None:
        """Initializes the SensorData.
        """
        # Measured distance
        self._distance = np.inf

        # Threading variables
        self._mutex = th.Lock()

    def get_distance(self) -> float:
        """Gets the current Euclidean distance between the sensor and the target.

        Returns:
            A float indicating the distance in meters [m].
        """
        # Acquires the mutex for the critical section
        self._mutex.acquire()

        # Reads the measured distance
        distance = self._distance

        # Releases the mutex
        self._mutex.release()

        return distance

    def set_distance(self, new_distance: float) -> None:
        """Sets the new measured distance between sensor and target.

        Args:
            new_distance: A float indicating the distance in meters [m].
        """
        # Acquires the mutex for the critical section
        self._mutex.acquire()

        # Sets the distance
        self._distance = new_distance

        # Releases the mutex
        self._mutex.release()
