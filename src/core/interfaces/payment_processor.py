"""
Payment processor interface.

ISP: This interface defines the contract for payment processing.
Different payment implementations can fulfill this interface.
"""

from abc import ABC, abstractmethod
from typing import Optional


class PaymentProcessor(ABC):
    """
    ISP: Interface for payment processing.

    Payment processors must:
    - Process payments
    - Handle refunds
    - Verify payment status
    """

    @abstractmethod
    def process_payment(
        self,
        booking_id: str,
        amount: float,
        payment_method: str,
        payment_details: dict,
    ) -> dict:
        """
        Process a payment for a booking.

        Args:
            booking_id: Booking identifier
            amount: Payment amount
            payment_method: Payment method identifier
            payment_details: Payment-specific details (card info, account, etc.)

        Returns:
            Payment result dictionary with transaction ID and status
        """
        pass

    @abstractmethod
    def refund_payment(self, transaction_id: str, amount: float) -> dict:
        """
        Refund a payment.

        Args:
            transaction_id: Transaction identifier
            amount: Refund amount

        Returns:
            Refund result dictionary
        """
        pass

    @abstractmethod
    def verify_payment_status(self, transaction_id: str) -> str:
        """
        Verify the status of a payment.

        Args:
            transaction_id: Transaction identifier

        Returns:
            Payment status (PENDING, COMPLETED, FAILED, etc.)
        """
        pass
