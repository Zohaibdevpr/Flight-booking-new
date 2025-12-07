"""
Passenger entity class.

SRP: Responsible only for representing passenger data and validation.
"""

from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class PassengerType(Enum):
    """Passenger type enumeration."""

    ADULT = "ADULT"
    CHILD = "CHILD"
    INFANT = "INFANT"


@dataclass
class Passenger:
    """
    SRP: Represents a passenger with essential identification and profile data.

    Responsibilities:
    - Store passenger information (name, email, phone, etc.)
    - Validate passenger data
    - Provide passenger profile information
    """

    passenger_id: str
    first_name: str
    last_name: str
    email: str
    phone: str
    date_of_birth: str
    passenger_type: PassengerType = PassengerType.ADULT
    loyalty_number: Optional[str] = None
    metadata: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate passenger data."""
        if not self.passenger_id:
            raise ValueError("Passenger ID cannot be empty")
        if not self.first_name or not self.last_name:
            raise ValueError("First name and last name are required")
        if not self.email or "@" not in self.email:
            raise ValueError("Valid email is required")
        if not self.phone:
            raise ValueError("Phone number is required")
        if not self.date_of_birth:
            raise ValueError("Date of birth is required")

    @property
    def full_name(self) -> str:
        """Get passenger's full name."""
        return f"{self.first_name} {self.last_name}"

    @property
    def contact_info(self) -> dict:
        """Get passenger's contact information."""
        return {
            "email": self.email,
            "phone": self.phone,
        }

    def update_email(self, new_email: str) -> None:
        """
        Update passenger email.

        Args:
            new_email: New email address

        Raises:
            ValueError: If email format is invalid
        """
        if not new_email or "@" not in new_email:
            raise ValueError("Valid email is required")
        self.email = new_email

    def update_phone(self, new_phone: str) -> None:
        """
        Update passenger phone number.

        Args:
            new_phone: New phone number

        Raises:
            ValueError: If phone is empty
        """
        if not new_phone:
            raise ValueError("Phone number cannot be empty")
        self.phone = new_phone

    def get_profile(self) -> dict:
        """
        Get passenger profile summary.

        Returns:
            Dictionary with passenger profile information
        """
        return {
            "id": self.passenger_id,
            "name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "type": self.passenger_type.value,
            "loyalty_number": self.loyalty_number,
        }
