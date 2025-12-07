"""
Window seat priority allocation strategy.

OCP: Concrete implementation of window-priority seating.
"""

from typing import List
from .base_strategy import SeatingStrategy


class WindowPriority(SeatingStrategy):
    """
    OCP: Window seat priority allocation strategy.

    This strategy prioritizes window seats (ending in A or F)
    over middle and aisle seats (B, C, D, E).
    """

    def allocate_seats(self, passenger_count: int) -> List[str]:
        """
        Allocate seats with window preference.

        Args:
            passenger_count: Number of seats to allocate

        Returns:
            List of allocated seat numbers (window seats first)
        """
        self.validate_seat_count(passenger_count)

        # Separate window and non-window seats
        window_seats = [seat for seat in self.available_seats if self._is_window_seat(seat)]
        non_window_seats = [
            seat for seat in self.available_seats if not self._is_window_seat(seat)
        ]

        # Allocate window seats first, then non-window
        allocated_seats = []

        # Add as many window seats as needed
        for seat in window_seats:
            if len(allocated_seats) < passenger_count:
                allocated_seats.append(seat)
            else:
                break

        # If more seats needed, add non-window seats
        for seat in non_window_seats:
            if len(allocated_seats) < passenger_count:
                allocated_seats.append(seat)
            else:
                break

        # Mark seats as used
        self.mark_seats_as_used(allocated_seats)

        return allocated_seats

    @staticmethod
    def _is_window_seat(seat: str) -> bool:
        """
        Check if seat is a window seat.

        Args:
            seat: Seat number (e.g., "1A", "1F")

        Returns:
            True if seat is a window seat
        """
        last_char = seat[-1].upper()
        return last_char in ["A", "F"]

    def get_strategy_name(self) -> str:
        """Get strategy name."""
        return "WINDOW_PRIORITY"

    def get_strategy_description(self) -> str:
        """Get strategy description."""
        return "Window seats allocated first, then other seats"
