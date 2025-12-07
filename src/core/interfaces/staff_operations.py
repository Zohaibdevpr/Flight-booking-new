"""
Staff operations interface.

ISP: This interface defines only operations that staff members need to perform.
Staff don't depend on passenger booking or admin system management interfaces.
"""

from abc import ABC, abstractmethod
from typing import List


class StaffOperations(ABC):
    """
    ISP: Interface for staff operations.

    Staff members can:
    - Check flight status
    - View passenger lists
    - Check passenger details
    - Process check-ins
    - Handle cancellations
    - Generate boarding passes
    """

    @abstractmethod
    def check_flight_status(self, flight_id: str) -> dict:
        """
        Check the current status of a flight.

        Args:
            flight_id: Flight identifier

        Returns:
            Flight status dictionary
        """
        pass

    @abstractmethod
    def get_passenger_list(self, flight_id: str) -> List[dict]:
        """
        Get list of passengers for a flight.

        Args:
            flight_id: Flight identifier

        Returns:
            List of passenger details
        """
        pass

    @abstractmethod
    def get_passenger_details(self, passenger_id: str) -> dict:
        """
        Get detailed information about a passenger.

        Args:
            passenger_id: Passenger identifier

        Returns:
            Passenger details dictionary
        """
        pass

    @abstractmethod
    def process_check_in(self, booking_id: str) -> bool:
        """
        Process passenger check-in.

        Args:
            booking_id: Booking identifier

        Returns:
            True if check-in was successful
        """
        pass

    @abstractmethod
    def generate_boarding_pass(self, booking_id: str) -> dict:
        """
        Generate a boarding pass for a booking.

        Args:
            booking_id: Booking identifier

        Returns:
            Boarding pass details dictionary
        """
        pass

    @abstractmethod
    def handle_cancellation_request(self, booking_id: str, reason: str) -> bool:
        """
        Handle a cancellation request from staff.

        Args:
            booking_id: Booking identifier
            reason: Reason for cancellation

        Returns:
            True if cancellation was processed successfully
        """
        pass
