"""
Flight entity class.

SRP: Responsible only for representing flight data and basic validation.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional


class FlightStatus(Enum):
    """Flight status enumeration."""

    SCHEDULED = "SCHEDULED"
    BOARDED = "BOARDED"
    DEPARTED = "DEPARTED"
    IN_FLIGHT = "IN_FLIGHT"
    LANDED = "LANDED"
    CANCELLED = "CANCELLED"


@dataclass
class Flight:
    """
    SRP: Represents a single flight with essential flight information.

    Responsibilities:
    - Store flight data (number, route, time, capacity, etc.)
    - Provide basic flight information
    - Track available seats
    """

    flight_number: str
    origin: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    aircraft_id: str
    total_seats: int
    available_seats: int
    status: FlightStatus = FlightStatus.SCHEDULED
    price: float = 0.0
    metadata: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate flight data."""
        if not self.flight_number:
            raise ValueError("Flight number cannot be empty")
        if self.origin == self.destination:
            raise ValueError("Origin and destination must be different")
        if self.departure_time >= self.arrival_time:
            raise ValueError("Departure time must be before arrival time")
        if self.total_seats <= 0:
            raise ValueError("Total seats must be positive")
        if self.available_seats > self.total_seats:
            raise ValueError("Available seats cannot exceed total seats")
        if self.available_seats < 0:
            raise ValueError("Available seats cannot be negative")

    def reserve_seat(self, count: int = 1) -> bool:
        """
        Reserve seats on the flight.

        Args:
            count: Number of seats to reserve

        Returns:
            True if reservation was successful, False otherwise
        """
        if count <= 0:
            raise ValueError("Reservation count must be positive")

        if self.available_seats >= count:
            self.available_seats -= count
            return True
        return False

    def cancel_reservation(self, count: int = 1) -> bool:
        """
        Cancel seat reservation.

        Args:
            count: Number of seats to release

        Returns:
            True if cancellation was successful, False otherwise
        """
        if count <= 0:
            raise ValueError("Cancellation count must be positive")

        if self.available_seats + count <= self.total_seats:
            self.available_seats += count
            return True
        return False

    def get_occupancy_rate(self) -> float:
        """
        Get the occupancy rate of the flight.

        Returns:
            Occupancy rate as a percentage (0-100)
        """
        if self.total_seats == 0:
            return 0.0
        return ((self.total_seats - self.available_seats) / self.total_seats) * 100

    @property
    def is_full(self) -> bool:
        """Check if flight has no available seats."""
        return self.available_seats == 0

    @property
    def departure_info(self) -> str:
        """Get formatted departure information."""
        return f"Flight {self.flight_number}: {self.origin} -> {self.destination} at {self.departure_time}"
