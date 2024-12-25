"""Estimator Package.

This package provides classes and modules for estimating the position
of a target object using distance measurements from multiple sensors.

Modules:
    multilateration: Defines the Multilateration class for estimating the 3D position of a target object.
"""

from .multilateration import Multilateration

__all__ = [
    "Multilateration",
]
