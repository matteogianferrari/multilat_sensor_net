"""This module implements the KalmanFilter class.

The KalmanFilter class provides an implementation of a Kalman Filter for tracking
and estimating the state of an object in 3D space. It uses a constant velocity model
to predict and correct the object's position and velocity over time.

Classes:
    KalmanFilter: KalmanFilter class for estimating and tracking the state of an object.

Usage Example:
    from multilat_sensor_net.client import KalmanFilter
    import time

    prev_time = time.time()

    obj = KalmanFilter()

    measurement = np.array([4.5, 2.5, 1.5])

    obj.set_state(measurement)

    curr_time = time.time()
    dt = curr_time - prev_time

    obj.update_matrices(dt)
    obj.predict()
    obj.update(measurement)

    pred_pos = obj.get_state()
"""

import numpy as np


class KalmanFilter:
    """KalmanFilter class for estimating and tracking the state of an object.

    This class implements a Kalman Filter using the constant velocity model to predict and correct
    the state of an object over time. The Kalman Filter estimates the position and velocity of the
    object and updates its predictions using new measurements. The class uses a state vector to
    represent the object's position and velocity, while leveraging matrices to manage uncertainty
    and model the system's dynamics effectively.

    Attributes:
        _x: A 6D numpy array indicating the state vector [x, y, z, v_x, v_y, v_z].
        _P: A 6x6 numpy matrix indicating the state covariance matrix.
        _F: A 6x6 numpy matrix indicating the update matrix.
        _Q: A 6x6 numpy matrix indicating the process covariance matrix.
        _R: A 3x3 numpy matrix indicating the sensor measurement covariance matrix.
        _y: A 3D numpy array storing the measurement residual (innovation).
        _S: A 3x3 numpy matrix indicating the innovation covariance matrix.
        _K: A 6x3 numpy matrix indicating the Kalman gain.
        _H: A 3x6 numpy matrix indicating the measurement matrix.
        _noise_ax: A float indicating the acceleration noise component for the X axis.
        _noise_ay: A float indicating the acceleration noise component for the Y axis.
        _noise_az: A float indicating the acceleration noise component for the Z axis.
    """

    def __init__(self) -> None:
        """Initializes the KalmanFilter.
        """
        # State vector [x, y, z, v_x, v_y, v_z]
        self._x = np.zeros(6)

        # Initializes the state covariance matrix.
        # The diagonal values of 1 for the position components [x, y, z] imply that there is
        # high confidence in the initial position estimates (low uncertainty).
        # The diagonal values of 100 for the velocity components [v_x, v_y, v_z] imply that
        # there is low confidence in the initial velocity estimates (high uncertainty).
        # The off-diagonal elements are set to 0, assuming no correlation between different state variables. 
        self._P = np.array([
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [0, 0, 0, 100, 0, 0],
            [0, 0, 0, 0, 100, 0],
            [0, 0, 0, 0, 0, 100]]
        )

        # Initializes the update matrix.
        # It is set to zeros initially because it depends on the delta time between measurements.
        self._F = np.zeros((6, 6))

        # Initializes the process covariance matrix.
        # This matrix represents the uncertainty in the system's process model (due to unknown accelerations).
        # It is set to zeros initially because it depends on the delta time between measurements.
        self._Q = np.zeros((6, 6))

        # Initializes the sensor measurement covariance matrix.
        # The values are set to be the squared variance of the measurement,
        # which is assumed to be +-40mm (depends on the sensor used).
        self._R = np.array([
            [0.0016, 0, 0],
            [0, 0.0016, 0],
            [0, 0, 0.0016]
        ])

        self._y = np.zeros(3)
        self._S = np.zeros(3)
        self._K = np.zeros(6)

        # Initializes the measurement matrix.
        # Maps the state vector (which includes both position and velocity) to the measurement vector.
        # The measurement vector only contains position (x, y, z), so the corresponding velocity
        # components in the state vector are ignored (set to 0).
        self._H = np.array([
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0]
        ])

        # Sets the acceleration noise components
        self._noise_ax = 2.
        self._noise_ay = 2.
        self._noise_az = 2.

    def set_state(self, pos: np.ndarray) -> None:
        """Sets the initial state of the tracked object.

        Args:
            pos: The tracked object initial position [x, y, z].
        """
        # The position contains x, y, z and the velocity must be set to 0
        self._x[0] = pos[0]
        self._x[1] = pos[1]
        self._x[2] = pos[2]
        self._x[3] = 0
        self._x[4] = 0
        self._x[5] = 0

    def get_state(self) -> np.array:
        """Gets the state of the tracked object.

        Only the position of the tracked object is required.

        Returns:
            A 3D numpy array containing the tracked object position [x, y, z].
        """
        return self._x[:2]
    
    def update_matrices(self, dt) -> None:
        """Updates the matrices that are dependent on a delta time.

        Updates the update matrix F and the process covariance matrix Q.
        This step is necessary to account for changes in the object's dynamics over time.

        Args:
            dt: A float indicating the delta time between measurements.
        """
        dt_2 = dt * dt
        dt_3 = dt_2 * dt
        dt_4 = dt_3 * dt

        # Updates the process covariance matrix
        self._Q = np.array([
            [dt_4 / 4. * self._noise_ax, 0., 0., dt_3 / 2. * self._noise_ax, 0., 0.],
            [0., dt_4 / 4. * self._noise_ay, 0., 0., dt_3 / 2. * self._noise_ay, 0.],
            [0., 0., dt_4 / 4. * self._noise_az, 0., 0., dt_3 / 2. * self._noise_az],
            [dt_3 / 2. * self._noise_ax, 0., 0., dt_2 * self._noise_ax, 0., 0.],
            [0., dt_3 / 2. * self._noise_ay, 0., 0., dt_2 * self._noise_ay, 0.],
            [0., 0., dt_3 / 2. * self._noise_az, 0., 0., dt_2 * self._noise_az]
        ])

        # Updates the update matrix
        self._F = np.array([
            [1, 0, 0, dt, 0, 0],
            [0, 1, 0, 0, dt, 0],
            [0, 0, 1, 0, 0, dt],
            [0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1]]
        )

    def predict(self) -> None:
        """Estimates the future state of the tracked object.
        """
        # State extrapolation equation
        self._x = self._F @ self._x

        # Covariance Extrapolation Equation
        self._P = self._F @ self._P @ self._F.T + self._Q

    def update(self, z: np.ndarray) -> None:
        """Corrects the estimation with the actual measurement.

        The update process requires the use of the measurement covariance matrix,
        which is defined for the sensor.

        Args:
            z: A 3D numpy array indicating the target position measurement [x, y, z].
        """
        # Measurement residual (innovation).
        # Difference between the actual measurement `z` and the predicted measurement.
        self._y = z - self._H @ self._x

        # Innovation covariance matrix.
        self._S = self._H @ self._P @ self._H.T + self._R

        # Kalman gain equation
        self._K = self._P @ self._H.T @ np.linalg.inv(self._S)

        I = np.eye(6)

        # State update equation
        self._x = self._x + self._K @ self._y

        # Covariance update equation
        self._P = (I - self._K @ self._H) @ self._P
