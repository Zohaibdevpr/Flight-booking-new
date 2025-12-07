"""
Base seating allocation strategy class.

OCP: Abstract base class that defines the seating allocation contract.
All seating strategies must inherit from this class and implement allocate_seats method.
"""

from abc import ABC, abstractmethod
from typing import List, Optional


class SeatingStrategy(ABC):
    """
    OCP: Abstract base class for all seating allocation strategies.

    This class defines the contract that all seating strategies must follow.
    New seating strategies can be added without modifying existing code.
    """

    def __init__(self, available_seats: List[str]):
        """
        Initialize seating strategy.

        Args:
            available_seats: List of available seat numbers
        """
        # Allow empty list for default initialization
        self.available_seats = available_seats.copy() if available_seats else []

    @abstractmethod
    def allocate_seats(self, passenger_count: int) -> List[str]:
        """
        Allocate seats for passengers based on strategy.

        Args:
            passenger_count: Number of seats to allocate

        Returns:
            List of allocated seat numbers

        Raises:
            ValueError: If not enough seats available
        """
        pass

    @abstractmethod
    def get_strategy_name(self) -> str:
        """
        Get the name of this seating strategy.

        Returns:
            Strategy name
        """
        pass

    @abstractmethod
    def get_strategy_description(self) -> str:
        """
        Get description of this seating strategy.

        Returns:
            Strategy description
        """
        pass

    def validate_seat_count(self, count: int) -> None:
        """
        Validate seat count request.

        Args:
            count: Number of seats requested

        Raises:
            ValueError: If count is invalid
        """
        if count <= 0:
            raise ValueError("Seat count must be positive")
        if count > len(self.available_seats):
            raise ValueError(
                f"Not enough seats available. Requested: {count}, Available: {len(self.available_seats)}"
            )

    def mark_seats_as_used(self, seats: List[str]) -> None:
        """
        Mark seats as used.

        Args:
            seats: List of seats to mark as used
        """
        for seat in seats:
            if seat in self.available_seats:
                self.available_seats.remove(seat)
