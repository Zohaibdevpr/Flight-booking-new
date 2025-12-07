"""
Family allocation strategy.

OCP: Concrete implementation of family-friendly seating.
"""

from typing import List
from .base_strategy import SeatingStrategy


class FamilyAllocation(SeatingStrategy):
    """
    OCP: Family-friendly seat allocation strategy.

    This strategy tries to keep family members together by allocating
    consecutive seats in the same row when possible.
    """

    def allocate_seats(self, passenger_count: int) -> List[str]:
        """
        Allocate seats to keep families together.

        Args:
            passenger_count: Number of seats to allocate

        Returns:
            List of allocated seat numbers (grouped together)
        """
        self.validate_seat_count(passenger_count)

        # Group seats by row
        seats_by_row = self._group_seats_by_row()

        allocated_seats = []

        # Try to allocate consecutive seats in the same row
        for row_number in sorted(seats_by_row.keys()):
            row_seats = seats_by_row[row_number]

            for seat in row_seats:
                if len(allocated_seats) < passenger_count:
                    allocated_seats.append(seat)
                else:
                    break

            if len(allocated_seats) >= passenger_count:
                break

        # Mark seats as used
        self.mark_seats_as_used(allocated_seats)

        return allocated_seats

    def _group_seats_by_row(self) -> dict:
        """
        Group available seats by row number.

        Returns:
            Dictionary with row numbers as keys and list of seats as values
        """
        seats_by_row = {}

        for seat in self.available_seats:
            # Extract row number (digits at the beginning)
            row_number = "".join(c for c in seat if c.isdigit())

            if row_number not in seats_by_row:
                seats_by_row[row_number] = []

            seats_by_row[row_number].append(seat)

        return seats_by_row

    def get_strategy_name(self) -> str:
        """Get strategy name."""
        return "FAMILY"

    def get_strategy_description(self) -> str:
        """Get strategy description."""
        return "Family-friendly allocation keeping passengers together"
