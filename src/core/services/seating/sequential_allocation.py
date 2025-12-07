"""
Sequential seat allocation strategy.

OCP: Concrete implementation of sequential seating.
"""

from typing import List
from .base_strategy import SeatingStrategy


class SequentialAllocation(SeatingStrategy):
    """
    OCP: Sequential seating allocation strategy.

    This strategy allocates seats in sequential order from the available seats list.
    Passengers get consecutive seats when possible.
    """

    def allocate_seats(self, passenger_count: int) -> List[str]:
        """
        Allocate seats sequentially.

        Args:
            passenger_count: Number of seats to allocate

        Returns:
            List of allocated seat numbers
        """
        self.validate_seat_count(passenger_count)

        # Get first N available seats
        allocated_seats = self.available_seats[:passenger_count]

        # Mark seats as used
        self.mark_seats_as_used(allocated_seats)

        return allocated_seats

    def get_strategy_name(self) -> str:
        """Get strategy name."""
        return "SEQUENTIAL"

    def get_strategy_description(self) -> str:
        """Get strategy description."""
        return "Sequential allocation of available seats"
