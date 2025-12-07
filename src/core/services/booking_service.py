"""
Booking service with dependency injection.

DIP: High-level module depends on abstractions (repositories, pricing strategies, notifiers, etc.),
not concrete implementations.
"""

from typing import List, Optional
from datetime import datetime
from ..entities import Booking, BookingStatus
from ..repositories import Repository
from .pricing import PricingStrategy, StandardPricing
from .seating import SeatingStrategy, SequentialAllocation


class BookingService:
    """
    DIP: Booking service with dependency injection.

    This service depends on abstractions for repositories, pricing strategies, and seating strategies.
    Implementations can be swapped without changing this service.
    """

    def __init__(
        self,
        booking_repository: Repository,
        pricing_strategy: Optional[PricingStrategy] = None,
        seating_strategy: Optional[SeatingStrategy] = None,
    ):
        """
        Initialize booking service with dependency injection.

        Args:
            booking_repository: Repository for storing bookings
            pricing_strategy: Pricing strategy to use (default: StandardPricing)
            seating_strategy: Seating strategy to use (default: SequentialAllocation)
        """
        if booking_repository is None:
            raise ValueError("Booking repository cannot be None")

        self.booking_repository = booking_repository
        self.pricing_strategy = pricing_strategy or StandardPricing(base_price=100.0)
        self.seating_strategy = seating_strategy or SequentialAllocation([])

    def create_booking(
        self,
        passenger_ids: List[str],
        flight_id: str,
        seat_numbers: Optional[List[str]] = None,
    ) -> Booking:
        """
        Create a new booking.

        Args:
            passenger_ids: List of passenger IDs
            flight_id: Flight ID
            seat_numbers: Specific seat numbers (optional)

        Returns:
            Created booking object
        """
        if not passenger_ids:
            raise ValueError("At least one passenger is required")

        if not flight_id:
            raise ValueError("Flight ID is required")

        booking_id = self._generate_booking_id()

        # Use provided seats or generate them
        if not seat_numbers:
            seat_numbers = self._allocate_seats(len(passenger_ids))

        booking = Booking(
            booking_id=booking_id,
            flight_id=flight_id,
            passenger_ids=passenger_ids,
            seat_numbers=seat_numbers,
            booking_date=datetime.now(),
            status=BookingStatus.PENDING,
        )

        self.booking_repository.add(booking_id, booking)
        return booking

    def confirm_booking(self, booking_id: str) -> bool:
        """
        Confirm a pending booking.

        Args:
            booking_id: Booking ID

        Returns:
            True if booking was confirmed
        """
        booking = self.booking_repository.get(booking_id)

        if not booking:
            raise ValueError(f"Booking not found: {booking_id}")

        booking.mark_as_confirmed()
        self.booking_repository.update(booking_id, booking)

        return True

    def pay_booking(self, booking_id: str, amount: float) -> bool:
        """
        Record payment for a booking.

        Args:
            booking_id: Booking ID
            amount: Payment amount

        Returns:
            True if payment was recorded
        """
        booking = self.booking_repository.get(booking_id)

        if not booking:
            raise ValueError(f"Booking not found: {booking_id}")

        booking.record_payment(amount)

        if booking.is_paid:
            booking.mark_as_paid()

        self.booking_repository.update(booking_id, booking)

        return True

    def check_in_booking(self, booking_id: str) -> bool:
        """
        Check in a paid booking.

        Args:
            booking_id: Booking ID

        Returns:
            True if check-in was successful
        """
        booking = self.booking_repository.get(booking_id)

        if not booking:
            raise ValueError(f"Booking not found: {booking_id}")

        booking.mark_as_checked_in()
        self.booking_repository.update(booking_id, booking)

        return True

    def cancel_booking(self, booking_id: str) -> bool:
        """
        Cancel a booking.

        Args:
            booking_id: Booking ID

        Returns:
            True if booking was cancelled
        """
        booking = self.booking_repository.get(booking_id)

        if not booking:
            raise ValueError(f"Booking not found: {booking_id}")

        booking.cancel()
        self.booking_repository.update(booking_id, booking)

        return True

    def get_booking(self, booking_id: str) -> Optional[Booking]:
        """
        Get a booking by ID.

        Args:
            booking_id: Booking ID

        Returns:
            Booking object or None if not found
        """
        return self.booking_repository.get(booking_id)

    def get_passenger_bookings(self, passenger_id: str) -> List[Booking]:
        """
        Get all bookings for a passenger.

        Args:
            passenger_id: Passenger ID

        Returns:
            List of bookings for the passenger
        """
        all_bookings = self.booking_repository.get_all()

        passenger_bookings = [
            booking for booking in all_bookings if passenger_id in booking.passenger_ids
        ]

        return passenger_bookings

    def calculate_booking_price(
        self,
        num_passengers: int,
        occupancy_rate: float = 50.0,
        days_until_departure: int = 30,
        passenger_type: str = "ADULT",
    ) -> float:
        """
        Calculate booking price using current pricing strategy.

        Args:
            num_passengers: Number of passengers
            occupancy_rate: Flight occupancy rate
            days_until_departure: Days until departure
            passenger_type: Type of passenger

        Returns:
            Total booking price
        """
        price_per_passenger = self.pricing_strategy.calculate_price(
            num_passengers, occupancy_rate, days_until_departure, passenger_type
        )

        return price_per_passenger * num_passengers

    def set_pricing_strategy(self, strategy: PricingStrategy) -> None:
        """
        Set a new pricing strategy.

        Args:
            strategy: Pricing strategy implementation
        """
        if strategy is None:
            raise ValueError("Pricing strategy cannot be None")

        self.pricing_strategy = strategy

    def set_seating_strategy(self, strategy: SeatingStrategy) -> None:
        """
        Set a new seating strategy.

        Args:
            strategy: Seating strategy implementation
        """
        if strategy is None:
            raise ValueError("Seating strategy cannot be None")

        self.seating_strategy = strategy

    def _generate_booking_id(self) -> str:
        """
        Generate a unique booking ID.

        Returns:
            Generated booking ID
        """
        import uuid

        return f"BK-{str(uuid.uuid4())[:8].upper()}"

    def _allocate_seats(self, seat_count: int) -> List[str]:
        """
        Allocate seats using current seating strategy.

        Args:
            seat_count: Number of seats to allocate

        Returns:
            List of allocated seat numbers
        """
        # In a real implementation, this would use the seating strategy
        # For now, generate sequential seat numbers
        return [f"{i+1}A" for i in range(seat_count)]
