"""Network Package.

This package provides classes and modules for managing a distributed network.
It includes functionality for maintaining network state, handling communication
between nodes, and estimating target positions.

Modules:
    network_data: Defines the NetworkData class for managing a thread-safe network state.
    network_service: Defines the NetworkService class for handling gRPC
        calls related to a distributed network.
    network_dealer: Defines the NetworkDealer class for managing the communication
        with distributed nodes via ZeroMQ.
    network_controller: Defines the NetworkController class as a facade for managing
        a distributed node and the related distance sensor.
"""

from .network_data import NetworkData
from .network_service import NetworkService
from .network_dealer import NetworkDealer
from .network_controller import NetworkController

__all__ = [
    "NetworkData",
    "NetworkService",
    "NetworkDealer",
    "NetworkController",
]
