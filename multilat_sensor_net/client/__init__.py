"""Client Package.

This package provides classes and modules for creating the client main application that requests
the target global position to a distributed network and tracks and predicts its future state using
a tracker.

Modules:
    kalman_filter: Defines the KalmanFilter class for estimating and tracking the state of an object.
    tracker: Defines the Tracker class for tracking a target and estimating its future state.
    client_app: Defines the ClientApp class for implementing the client application.
"""

from .kalman_filter import KalmanFilter
from .tracker import Tracker
from .client_app import ClientApp

__all__ = [
    "KalmanFilter",
    "Tracker",
    "ClientApp",
]
