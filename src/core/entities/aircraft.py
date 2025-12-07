"""
Aircraft entity classes demonstrating LSP (Liskov Substitution Principle).

LSP: All aircraft types must be substitutable for the base Aircraft class.
All aircraft maintain the contract: they must have seats and capacity.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Aircraft(ABC):
    """
    LSP: Abstract base class for all aircraft types.

    This class defines the contract that all aircraft implementations must follow.
    Any subclass must be fully substitutable for the base class without breaking functionality.
    """

    aircraft_id: str
    model: str
    manufacturer: str
    total_seats: int
    seats_layout: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate aircraft data."""
        if not self.aircraft_id:
            raise ValueError("Aircraft ID cannot be empty")
        if not self.model:
            raise ValueError("Aircraft model cannot be empty")
        if self.total_seats < 0:
            raise ValueError("Total seats cannot be negative")

    @abstractmethod
    def get_seat_classes(self) -> List[str]:
        """
        Get available seat classes for this aircraft.

        Returns:
            List of seat class names
        """
        pass

    @abstractmethod
    def get_seats_by_class(self, seat_class: str) -> int:
        """
        Get number of seats for a specific class.

        Args:
            seat_class: The seat class name

        Returns:
            Number of seats in that class
        """
        pass

    @abstractmethod
    def calculate_luggage_allowance(self) -> float:
        """
        Calculate luggage allowance in kg for this aircraft.

        Returns:
            Luggage allowance in kg
        """
        pass

    def get_info(self) -> dict:
        """
        Get aircraft information.

        Returns:
            Dictionary with aircraft information
        """
        return {
            "aircraft_id": self.aircraft_id,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "total_seats": self.total_seats,
            "seat_classes": self.get_seat_classes(),
        }


@dataclass
class CommercialAircraft(Aircraft):
    """
    LSP: Concrete implementation of commercial passenger aircraft.

    This aircraft type is fully substitutable for the base Aircraft class.
    It implements all abstract methods and maintains the contract.
    """

    first_class_seats: int = 12
    business_class_seats: int = 48
    economy_class_seats: int = 240

    def __post_init__(self) -> None:
        """Validate commercial aircraft data."""
        # Ensure seat count matches configuration
        if (
            self.first_class_seats
            + self.business_class_seats
            + self.economy_class_seats
            != self.total_seats
        ):
            raise ValueError("Seat distribution does not match total seats")
        super().__post_init__()

    def get_seat_classes(self) -> List[str]:
        """Get available seat classes."""
        return ["FIRST", "BUSINESS", "ECONOMY"]

    def get_seats_by_class(self, seat_class: str) -> int:
        """
        Get number of seats for a specific class.

        Args:
            seat_class: The seat class name

        Returns:
            Number of seats in that class
        """
        class_map = {
            "FIRST": self.first_class_seats,
            "BUSINESS": self.business_class_seats,
            "ECONOMY": self.economy_class_seats,
        }
        if seat_class not in class_map:
            raise ValueError(f"Unknown seat class: {seat_class}")
        return class_map[seat_class]

    def calculate_luggage_allowance(self) -> float:
        """
        Calculate luggage allowance for commercial aircraft.

        Returns:
            Luggage allowance in kg
        """
        return 25.0  # kg per passenger


@dataclass
class CargoPlanee(Aircraft):
    """
    LSP: Concrete implementation of cargo aircraft.

    This aircraft type is fully substitutable for the base Aircraft class.
    Even though it doesn't have traditional "seats", it maintains the same interface
    by representing cargo capacity in equivalent units.
    """

    cargo_capacity_kg: float = 50000.0

    def __post_init__(self) -> None:
        """Validate cargo aircraft data."""
        if self.cargo_capacity_kg <= 0:
            raise ValueError("Cargo capacity must be positive")
        # Ensure total_seats is 0 for cargo aircraft
        if self.total_seats != 0:
            raise ValueError("Cargo aircraft must have 0 total seats")
        super().__post_init__()

    def get_seat_classes(self) -> List[str]:
        """
        Get available seat classes.

        Returns:
            Empty list as cargo aircraft don't have typical seat classes
        """
        return []

    def get_seats_by_class(self, seat_class: str) -> int:
        """
        Get number of seats for a specific class.

        Args:
            seat_class: The seat class name

        Returns:
            0 as cargo aircraft don't have seats
        """
        return 0

    def calculate_luggage_allowance(self) -> float:
        """
        Calculate luggage allowance for cargo aircraft.

        Returns:
            Total cargo capacity in kg
        """
        return self.cargo_capacity_kg

    def add_cargo(self, weight_kg: float) -> bool:
        """
        Add cargo to the aircraft.

        Args:
            weight_kg: Weight of cargo to add

        Returns:
            True if cargo was added successfully
        """
        if weight_kg <= 0:
            raise ValueError("Cargo weight must be positive")
        # Implementation would track actual cargo
        return True
