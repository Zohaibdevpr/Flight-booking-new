"""
Flight type classifications.

LSP: Different flight types that can be used interchangeably in the system.
"""

from enum import Enum


class FlightType(Enum):
    """Flight type enumeration for categorizing flights."""

    DOMESTIC = "DOMESTIC"
    INTERNATIONAL = "INTERNATIONAL"
    REGIONAL = "REGIONAL"
    CHARTER = "CHARTER"
