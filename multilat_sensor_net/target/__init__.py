"""Target Package.

This package provides classes and modules for managing a target in a 3D space, including
domain logic, network services, and position updating mechanisms.

Modules:
    target_object: Defines the TargetData class for managing target state.
    target_service: Defines the TargetService class for handling gRPC server interactions.
    target_updater: Defines the TargetUpdater class for updating the target's position based on a trajectory.
    target_controller: Defines the TargetController class as a facade integrating domain logic, services, and updaters.
"""

from .target_data import TargetData
from .target_service import TargetService
from .target_updater import TargetUpdater
from .target_controller import TargetController

__all__ = [
    "TargetData",
    "TargetService",
    "TargetUpdater",
    "TargetController",
]
