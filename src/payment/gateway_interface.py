"""
Payment gateway interface.

DIP: Abstract interface for all payment gateways.
Different payment providers implement this interface.
"""

from abc import ABC, abstractmethod
from typing import Optional


class PaymentGateway(ABC):
    """
    DIP: Abstract interface for payment gateways.

    All payment providers must implement this interface.
    High-level modules depend on this abstraction, not specific implementations.
    """

    @abstractmethod
    def process_payment(
        self,
        transaction_id: str,
        amount: float,
        currency: str,
        customer_details: dict,
        payment_details: dict,
    ) -> dict:
        """
        Process a payment transaction.

        Args:
            transaction_id: Unique transaction identifier
            amount: Payment amount
            currency: Currency code (USD, EUR, etc.)
            customer_details: Customer information (name, email, etc.)
            payment_details: Payment-specific details (card, account, etc.)

        Returns:
            Result dictionary with transaction status and reference
        """
        pass

    @abstractmethod
    def refund_payment(
        self, reference_id: str, amount: float, reason: str
    ) -> dict:
        """
        Refund a payment.

        Args:
            reference_id: Original transaction reference ID
            amount: Refund amount
            reason: Reason for refund

        Returns:
            Result dictionary with refund status
        """
        pass

    @abstractmethod
    def verify_payment(self, reference_id: str) -> dict:
        """
        Verify payment status.

        Args:
            reference_id: Transaction reference ID

        Returns:
            Result dictionary with payment status
        """
        pass

    @abstractmethod
    def get_gateway_name(self) -> str:
        """
        Get payment gateway name.

        Returns:
            Gateway name
        """
        pass
