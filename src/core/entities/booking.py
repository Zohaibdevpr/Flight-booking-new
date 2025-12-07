"""
Booking entity class.

SRP: Responsible only for representing booking data and basic booking operations.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional


class BookingStatus(Enum):
    """Booking status enumeration."""

    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    PAID = "PAID"
    CHECKED_IN = "CHECKED_IN"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


@dataclass
class Booking:
    """
    SRP: Represents a booking with essential booking information.

    Responsibilities:
    - Store booking data (ID, flight, passengers, seats, etc.)
    - Track booking status
    - Manage booking lifecycle (creation, cancellation, completion)
    """

    booking_id: str
    flight_id: str
    passenger_ids: List[str]
    seat_numbers: List[str]
    booking_date: datetime
    status: BookingStatus = BookingStatus.PENDING
    total_price: float = 0.0
    paid_amount: float = 0.0
    payment_method: Optional[str] = None
    metadata: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate booking data."""
        if not self.booking_id:
            raise ValueError("Booking ID cannot be empty")
        if not self.flight_id:
            raise ValueError("Flight ID cannot be empty")
        if not self.passenger_ids:
            raise ValueError("At least one passenger is required")
        if not self.seat_numbers:
            raise ValueError("At least one seat is required")
        if len(self.passenger_ids) != len(self.seat_numbers):
            raise ValueError("Number of passengers must match number of seats")
        if self.total_price < 0:
            raise ValueError("Total price cannot be negative")
        if self.paid_amount < 0:
            raise ValueError("Paid amount cannot be negative")
        if self.paid_amount > self.total_price:
            raise ValueError("Paid amount cannot exceed total price")

    def mark_as_confirmed(self) -> None:
        """Mark booking as confirmed."""
        if self.status != BookingStatus.PENDING:
            raise ValueError(
                f"Cannot confirm booking with status: {self.status.value}"
            )
        self.status = BookingStatus.CONFIRMED

    def mark_as_paid(self) -> None:
        """Mark booking as paid."""
        if self.status != BookingStatus.CONFIRMED:
            raise ValueError(
                f"Cannot mark as paid with status: {self.status.value}"
            )
        self.status = BookingStatus.PAID

    def mark_as_checked_in(self) -> None:
        """Mark booking as checked in."""
        if self.status != BookingStatus.PAID:
            raise ValueError(
                f"Cannot check in with status: {self.status.value}"
            )
        self.status = BookingStatus.CHECKED_IN

    def mark_as_completed(self) -> None:
        """Mark booking as completed."""
        if self.status != BookingStatus.CHECKED_IN:
            raise ValueError(
                f"Cannot complete with status: {self.status.value}"
            )
        self.status = BookingStatus.COMPLETED

    def cancel(self) -> None:
        """Cancel the booking."""
        if self.status in [BookingStatus.COMPLETED, BookingStatus.CANCELLED]:
            raise ValueError(
                f"Cannot cancel booking with status: {self.status.value}"
            )
        self.status = BookingStatus.CANCELLED

    @property
    def is_paid(self) -> bool:
        """Check if booking is fully paid."""
        return self.paid_amount >= self.total_price

    @property
    def remaining_balance(self) -> float:
        """Get remaining balance to be paid."""
        return max(0.0, self.total_price - self.paid_amount)

    def record_payment(self, amount: float) -> bool:
        """
        Record a payment for this booking.

        Args:
            amount: Payment amount

        Returns:
            True if payment was recorded successfully
        """
        if amount <= 0:
            raise ValueError("Payment amount must be positive")

        if self.paid_amount + amount <= self.total_price:
            self.paid_amount += amount
            return True
        return False

    def get_summary(self) -> dict:
        """
        Get booking summary.

        Returns:
            Dictionary with booking summary information
        """
        return {
            "booking_id": self.booking_id,
            "flight_id": self.flight_id,
            "passenger_count": len(self.passenger_ids),
            "seats": self.seat_numbers,
            "status": self.status.value,
            "total_price": self.total_price,
            "paid_amount": self.paid_amount,
            "remaining_balance": self.remaining_balance,
            "is_paid": self.is_paid,
        }
