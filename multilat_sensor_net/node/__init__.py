"""Node Package.

This package provides classes and modules for managing distributed nodes in a sensor network.
It enables communication, coordination, and control of nodes, integrating
distance sensors and network functionalities.

Modules:
    node_stub: Defines the NodeStub class for handling communication between
        a node and the distributed network via gRPC.
    node_router: Defines the NodeRouter class for managing communication between
        node and the distributed network using ZeroMQ.
    node_controller: Define the NodeController class as a facade for managing
        a distributed node and the related distance sensor.
"""

from .node_stub import NodeStub
from .node_router import NodeRouter
from .node_controller import NodeController

__all__ = [
    "NodeStub",
    "NodeRouter",
    "NodeController",
]
