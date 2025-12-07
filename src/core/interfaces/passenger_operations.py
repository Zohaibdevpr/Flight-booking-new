"""
Passenger operations interface.

ISP: This interface defines only operations that passengers need to perform.
Passengers don't depend on admin or staff operations.
"""

from abc import ABC, abstractmethod
from typing import List, Optional


class PassengerOperations(ABC):
    """
    ISP: Interface for passenger operations.

    Passengers can:
    - Search for flights
    - View flight details
    - Make bookings
    - View their bookings
    - Cancel bookings
    - Check booking status
    """

    @abstractmethod
    def search_flights(
        self,
        origin: str,
        destination: str,
        departure_date: str,
        return_date: Optional[str] = None,
    ) -> List[dict]:
        """
        Search for available flights.

        Args:
            origin: Departure city
            destination: Arrival city
            departure_date: Departure date in YYYY-MM-DD format
            return_date: Return date for round trips (optional)

        Returns:
            List of available flights
        """
        pass

    @abstractmethod
    def get_flight_details(self, flight_id: str) -> dict:
        """
        Get detailed information about a flight.

        Args:
            flight_id: The flight identifier

        Returns:
            Flight details dictionary
        """
        pass

    @abstractmethod
    def make_booking(
        self,
        passenger_id: str,
        flight_id: str,
        seat_numbers: List[str],
        pricing_strategy: str = "standard",
    ) -> str:
        """
        Make a new booking.

        Args:
            passenger_id: Passenger identifier
            flight_id: Flight identifier
            seat_numbers: List of seat numbers to book
            pricing_strategy: Pricing strategy to use

        Returns:
            Booking ID
        """
        pass

    @abstractmethod
    def view_my_bookings(self, passenger_id: str) -> List[dict]:
        """
        View all bookings for a passenger.

        Args:
            passenger_id: Passenger identifier

        Returns:
            List of booking details
        """
        pass

    @abstractmethod
    def cancel_booking(self, booking_id: str) -> bool:
        """
        Cancel an existing booking.

        Args:
            booking_id: Booking identifier

        Returns:
            True if cancellation was successful
        """
        pass

    @abstractmethod
    def check_booking_status(self, booking_id: str) -> str:
        """
        Check the status of a booking.

        Args:
            booking_id: Booking identifier

        Returns:
            Current booking status
        """
        pass
