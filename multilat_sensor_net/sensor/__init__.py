"""Sensor Package.

This package provides classes and modules for managing distance sensors in a 3D space.
It offers tools for measuring distances, updating sensor states, and controlling sensor operations.

Modules:
    sensor_object: Defines the SensorData class for managing a distance sensor state.
    sensor_updater: Defines the SensorUpdater class for measuring the Euclidean distance to the target.
    sensor_controller: Defines the SensorController as a facade for managing a distance sensor in a 3D space.
"""

from .sensor_data import SensorData
from .sensor_updater import SensorUpdater
from .sensor_controller import SensorController

__all__ = [
    "SensorData",
    "SensorUpdater",
    "SensorController",
]
