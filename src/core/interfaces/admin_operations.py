"""
Admin operations interface.

ISP: This interface defines only operations that administrators need to perform.
Admins don't depend on passenger booking operations.
"""

from abc import ABC, abstractmethod
from typing import List, Optional


class AdminOperations(ABC):
    """
    ISP: Interface for administrative operations.

    Administrators can:
    - Add/update flights
    - Add/update aircraft
    - Manage pricing strategies
    - Generate reports
    - View system statistics
    - Manage users
    """

    @abstractmethod
    def add_flight(
        self,
        flight_number: str,
        origin: str,
        destination: str,
        departure_time: str,
        arrival_time: str,
        aircraft_id: str,
        price: float,
    ) -> str:
        """
        Add a new flight to the system.

        Args:
            flight_number: Unique flight number
            origin: Departure city
            destination: Arrival city
            departure_time: Departure time in ISO format
            arrival_time: Arrival time in ISO format
            aircraft_id: Aircraft identifier
            price: Base ticket price

        Returns:
            Flight ID
        """
        pass

    @abstractmethod
    def add_aircraft(
        self, aircraft_type: str, model: str, manufacturer: str, total_seats: int
    ) -> str:
        """
        Add a new aircraft to the system.

        Args:
            aircraft_type: Type of aircraft (COMMERCIAL, CARGO, etc.)
            model: Aircraft model
            manufacturer: Aircraft manufacturer
            total_seats: Total seat count

        Returns:
            Aircraft ID
        """
        pass

    @abstractmethod
    def set_pricing_strategy(self, flight_id: str, strategy: str) -> bool:
        """
        Set the pricing strategy for a flight.

        Args:
            flight_id: Flight identifier
            strategy: Pricing strategy name (STANDARD, DYNAMIC, SEASONAL, LOYALTY)

        Returns:
            True if strategy was set successfully
        """
        pass

    @abstractmethod
    def get_revenue_report(
        self, start_date: str, end_date: str
    ) -> dict:
        """
        Generate revenue report for a date range.

        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format

        Returns:
            Revenue report dictionary
        """
        pass

    @abstractmethod
    def get_system_statistics(self) -> dict:
        """
        Get overall system statistics.

        Returns:
            System statistics dictionary
        """
        pass

    @abstractmethod
    def get_flight_occupancy_report(self) -> List[dict]:
        """
        Get occupancy report for all flights.

        Returns:
            List of flight occupancy information
        """
        pass
