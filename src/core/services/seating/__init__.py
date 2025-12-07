"""
Seating allocation strategies.

OCP: Open/Closed Principle - The system is open for extension (new seating strategies)
but closed for modification (existing strategies don't need to change).
"""

from .base_strategy import SeatingStrategy
from .sequential_allocation import SequentialAllocation
from .window_priority import WindowPriority
from .family_allocation import FamilyAllocation

__all__ = [
    "SeatingStrategy",
    "SequentialAllocation",
    "WindowPriority",
    "FamilyAllocation",
]
