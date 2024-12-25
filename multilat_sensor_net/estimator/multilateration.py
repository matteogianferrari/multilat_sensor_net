"""This module implements the Multilateration class.

The Multilateration class estimates the position of a target object based on distance measurements
from multiple sensors with known positions. The class uses nonlinear least squares optimization
to minimize errors in the estimated position.

Classes:
    Multilateration: Multilateration class for estimating the 3D position of a target object.

Usage Example:
    from multilat_sensor_net.estimator import Multilateration
    import numpy as np

    # Define sensor positions
    sensors = {
        1: (np.array([0.0, 0.0, 0.0]),),
        2: (np.array([1.0, 0.0, 0.0]),),
        3: (np.array([0.0, 1.0, 0.0]),)
    }

    # Provide distance measurements
    distances = {
        1: 1.0,
        2: 1.414,
        3: 1.414
    }

    # Initialize the multilateration object
    obj = Multilateration(verbose=False)
    obj.set_sensor_positions(sensors)

    position = obj.estimate_position(distances)  # Output: array([3., 3., 10.])
"""

from scipy.optimize import least_squares
import numpy as np


class Multilateration:
    """Multilateration class for estimating the 3D position of a target object.

    This class determines the position of a target object using the distances measured by
    multiple sensors placed at known positions. It employs nonlinear least squares
    optimization to minimize the residuals between predicted and measured distances.

    Attributes:
        verbose: A boolean flag that enables logging for debugging purposes. If True, detailed
            logs about actions performed by the components will be printed to the console.
        _sensor_positions: A dictionary mapping sensor IDs to their 3D positions as numpy arrays.
        _initial_guess: A numpy array representing the initial guess for the target's position.
    """
    
    def __init__(self, verbose: bool) -> None:
        """Initializes the Multilateration class.

        Args:
            verbose: Flag indicating whether the classes must produce an output.
        """
        self._sensor_positions = {}
        self._initial_guess = np.array([0., 0., 0.])

        # Logging attributes
        self.verbose = verbose

    def set_sensor_positions(self, nodes_info: dict) -> None:
        """Sets the positions of the sensors based on the provided node information.

        Args:
            nodes_info: A dictionary where each key is a sensor ID and the value is
                a tuple containing the sensor's 3D position as a numpy array.
        """
        for node_data in nodes_info.items():
            # Extract the values
            node_id = node_data[0]
            node_pos = node_data[1][0]

            self._sensor_positions[node_id] = node_pos

    def estimate_position(self, distances: dict) -> np.array:
        """Estimates the target position based on sensor measurements.

        This method uses a nonlinear least squares approach to minimize the residuals
        between the predicted and measured distances from each sensor.

        Args:
            distances: A dictionary mapping sensor IDs to measured distances from the target.

        Returns:
            A numpy array representing the estimated 3D position of the target.
        """
        # Define an objective function that returns the residual vector.
        # For each sensor i, residual_i = ||pos - p_i|| - d_i
        # least_squares automatically sums the squares of these residuals.
        def objective_function(pos):
            residuals = []
            for sensor_id, sensor_pos in self._sensor_positions.items():
                if sensor_id in distances:
                    measured_distance = distances[sensor_id]
                    # Computes the Euclidean distance from the current guess to sensor_pos
                    predicted_distance = np.linalg.norm(pos - sensor_pos)
                    residuals.append(predicted_distance - measured_distance)
            return residuals

        # Minimizes the objective function to estimate the object's position
        result = least_squares(objective_function, self._initial_guess)

        # Extracts the optimized position and updates the initial guess for future runs
        self._initial_guess = result.x

        if self.verbose:
            print(f"Estimated Position of target object: {self._initial_guess[0]}")

        return self._initial_guess
