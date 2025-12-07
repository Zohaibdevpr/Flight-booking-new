"""
Flight service with dependency injection.

DIP: High-level module depends on abstractions (repositories, notifiers, etc.),
not concrete implementations.
"""

from typing import List, Optional
from ..entities import Flight, FlightStatus
from ..repositories import Repository


class FlightService:
    """
    DIP: Flight service with dependency injection.

    This service depends on abstractions (Repository) rather than concrete implementations.
    The Repository implementation can be swapped without changing this service.
    """

    def __init__(self, flight_repository: Repository):
        """
        Initialize flight service with dependency injection.

        Args:
            flight_repository: Repository implementation for storing flights
        """
        if flight_repository is None:
            raise ValueError("Flight repository cannot be None")
        self.flight_repository = flight_repository

    def add_flight(self, flight: Flight) -> bool:
        """
        Add a new flight to the system.

        Args:
            flight: Flight object to add

        Returns:
            True if flight was added successfully
        """
        if not flight:
            raise ValueError("Flight cannot be None")

        try:
            self.flight_repository.add(flight.flight_number, flight)
            return True
        except ValueError as e:
            raise ValueError(f"Failed to add flight: {str(e)}")

    def get_flight(self, flight_number: str) -> Optional[Flight]:
        """
        Get a flight by flight number.

        Args:
            flight_number: The flight number

        Returns:
            Flight object or None if not found
        """
        return self.flight_repository.get(flight_number)

    def get_all_flights(self) -> List[Flight]:
        """
        Get all flights.

        Returns:
            List of all flights
        """
        return self.flight_repository.get_all()

    def search_flights(
        self,
        origin: str,
        destination: str,
        min_available_seats: int = 1,
    ) -> List[Flight]:
        """
        Search for flights by origin and destination.

        Args:
            origin: Departure city
            destination: Arrival city
            min_available_seats: Minimum available seats required

        Returns:
            List of matching flights
        """
        all_flights = self.flight_repository.get_all()

        matching_flights = [
            flight
            for flight in all_flights
            if flight.origin.lower() == origin.lower()
            and flight.destination.lower() == destination.lower()
            and flight.available_seats >= min_available_seats
            and flight.status == FlightStatus.SCHEDULED
        ]

        return matching_flights

    def reserve_seats(self, flight_number: str, seat_count: int) -> bool:
        """
        Reserve seats on a flight.

        Args:
            flight_number: Flight number
            seat_count: Number of seats to reserve

        Returns:
            True if reservation was successful
        """
        flight = self.flight_repository.get(flight_number)

        if not flight:
            raise ValueError(f"Flight not found: {flight_number}")

        success = flight.reserve_seat(seat_count)

        if success:
            self.flight_repository.update(flight_number, flight)

        return success

    def cancel_reservation(self, flight_number: str, seat_count: int) -> bool:
        """
        Cancel seat reservation on a flight.

        Args:
            flight_number: Flight number
            seat_count: Number of seats to release

        Returns:
            True if cancellation was successful
        """
        flight = self.flight_repository.get(flight_number)

        if not flight:
            raise ValueError(f"Flight not found: {flight_number}")

        success = flight.cancel_reservation(seat_count)

        if success:
            self.flight_repository.update(flight_number, flight)

        return success

    def get_occupancy_report(self) -> List[dict]:
        """
        Get occupancy report for all flights.

        Returns:
            List of flight occupancy information
        """
        all_flights = self.flight_repository.get_all()

        report = [
            {
                "flight_number": flight.flight_number,
                "origin": flight.origin,
                "destination": flight.destination,
                "total_seats": flight.total_seats,
                "available_seats": flight.available_seats,
                "occupied_seats": flight.total_seats - flight.available_seats,
                "occupancy_rate": flight.get_occupancy_rate(),
                "status": flight.status.value,
            }
            for flight in all_flights
        ]

        return report
