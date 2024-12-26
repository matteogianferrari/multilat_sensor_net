"""This module implements the Tracker class.

The Tracker class provides an implementation for tracking an object and estimating its future state
using a Kalman Filter. It processes position measurements of a target in 3D space and predicts
its motion over time.

Classes:
    Tracker: Tracker class for tracking an object and estimating its future state.

Usage Example:
    from multilat_sensor_net.client import Tracker

    obj = Tracker()

    obj.tracker_core(measurement=np.array([4.5, 2.5, 1.5]))

    pred_pos = obj.get_predicted_position() # Output: array([4.5, 2.5, 1.5])
"""

from multilat_sensor_net.client import KalmanFilter
import numpy as np
import time


class Tracker:
    """Tracker class for tracking a target and estimating its future state.

    This class receives messages containing the measurement of a target position in a 3D space
    and tracks it over time using a Kalman Filter to predict its future state.

    Attributes:
        _kalman: A KalmanFilter instance for estimating the target position.
        _is_initialized: A bool used to check for initialization of the tracked object.
        _prev_time: A float indicating the previous timestamp to update the Kalman Filter matrices.
        _pred_pos: A 3D numpy array indicating the tracked object position [x, y, z].
    """

    def __init__(self) -> None:
        """Initializes the Tracker.
        """
        # Kalman attributes
        self._kalman = KalmanFilter()
        self._kalman.set_state(np.array([0., 0., 0.]))

        # Tracker attributes
        self._is_initialized = False
        self._prev_time = time.time()
        self._pred_pos = None

    def tracker_core(self, measurement: np.array) -> None:
        """Executes the logic of the tracker.

        Args:
            measurement: A 3D numpy array containing the measured target position.
        """
        # Checks if the kalman filter has been already initialized
        if not self._is_initialized:
            self._is_initialized = True
            self._kalman.set_state(measurement)

        # Computes dt
        curr_time = time.time()
        dt = curr_time - self._prev_time
        self._prev_time = curr_time

        # Updates the matrices
        self._kalman.update_matrices(dt)

        # Predicts the future position of the target
        self._kalman.predict()

        # Updates the prediction with the measurement from the distributed network
        self._kalman.update(measurement)

        # Gets the estimated position and records it
        self._pred_pos = self._kalman.get_state()

    def get_predicted_position(self) -> np.array:
        """Gets the predicted target position.

        Returns:
            A 3D numpy array containing the predicted target position [x, y, z].
        """
        return self._pred_pos
