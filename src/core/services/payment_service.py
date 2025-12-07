"""
Payment service with dependency injection.

DIP: High-level module depends on abstractions (payment gateways, notifiers),
not concrete implementations.
"""

from typing import Optional
from ..entities import Booking
from ...payment import PaymentGateway
from ..services.notification import BaseNotifier


class PaymentService:
    """
    DIP: Payment service with dependency injection.

    This service depends on abstractions for payment gateways and notifiers.
    Different payment providers can be used without changing this service.
    """

    def __init__(
        self,
        payment_gateway: PaymentGateway,
        notifier: Optional[BaseNotifier] = None,
    ):
        """
        Initialize payment service with dependency injection.

        Args:
            payment_gateway: Payment gateway implementation
            notifier: Notifier for sending payment confirmations (optional)
        """
        if payment_gateway is None:
            raise ValueError("Payment gateway cannot be None")

        self.payment_gateway = payment_gateway
        self.notifier = notifier

    def process_booking_payment(
        self,
        booking: Booking,
        customer_details: dict,
        payment_details: dict,
        currency: str = "USD",
    ) -> dict:
        """
        Process payment for a booking.

        Args:
            booking: Booking object
            customer_details: Customer information
            payment_details: Payment details (card, account, etc.)
            currency: Currency code

        Returns:
            Payment result dictionary
        """
        if not booking:
            raise ValueError("Booking cannot be None")

        if not customer_details:
            raise ValueError("Customer details are required")

        if not payment_details:
            raise ValueError("Payment details are required")

        # Process payment through gateway
        result = self.payment_gateway.process_payment(
            transaction_id=booking.booking_id,
            amount=booking.total_price,
            currency=currency,
            customer_details=customer_details,
            payment_details=payment_details,
        )

        # Send notification if notifier is available
        if self.notifier and result.get("status") == "SUCCESS":
            self._send_payment_confirmation(booking, result)

        return result

    def refund_booking_payment(
        self,
        booking: Booking,
        reference_id: str,
        reason: str = "Customer request",
    ) -> dict:
        """
        Refund payment for a booking.

        Args:
            booking: Booking object
            reference_id: Original transaction reference ID
            reason: Reason for refund

        Returns:
            Refund result dictionary
        """
        if not booking:
            raise ValueError("Booking cannot be None")

        if not reference_id:
            raise ValueError("Reference ID is required")

        # Process refund through gateway
        result = self.payment_gateway.refund_payment(
            reference_id=reference_id,
            amount=booking.paid_amount,
            reason=reason,
        )

        # Send notification if notifier is available
        if self.notifier and result.get("status") == "SUCCESS":
            self._send_refund_notification(booking, result)

        return result

    def verify_payment(self, reference_id: str) -> dict:
        """
        Verify payment status.

        Args:
            reference_id: Transaction reference ID

        Returns:
            Payment status dictionary
        """
        if not reference_id:
            raise ValueError("Reference ID is required")

        return self.payment_gateway.verify_payment(reference_id)

    def set_payment_gateway(self, gateway: PaymentGateway) -> None:
        """
        Set a new payment gateway.

        Args:
            gateway: Payment gateway implementation
        """
        if gateway is None:
            raise ValueError("Payment gateway cannot be None")

        self.payment_gateway = gateway

    def set_notifier(self, notifier: Optional[BaseNotifier]) -> None:
        """
        Set a notifier for sending confirmations.

        Args:
            notifier: Notifier implementation or None
        """
        self.notifier = notifier

    def _send_payment_confirmation(self, booking: Booking, payment_result: dict) -> None:
        """
        Send payment confirmation notification.

        Args:
            booking: Booking object
            payment_result: Payment result from gateway
        """
        if not self.notifier:
            return

        message = (
            f"Payment of {booking.total_price} USD has been processed successfully. "
            f"Reference ID: {payment_result.get('reference_id')}"
        )

        try:
            self.notifier.send_notification(
                recipient=booking.booking_id,
                subject="Payment Confirmation",
                message=message,
                notification_type="PAYMENT",
            )
        except Exception:
            pass  # Silently fail if notification can't be sent

    def _send_refund_notification(self, booking: Booking, refund_result: dict) -> None:
        """
        Send refund notification.

        Args:
            booking: Booking object
            refund_result: Refund result from gateway
        """
        if not self.notifier:
            return

        message = (
            f"Refund of {refund_result.get('refund_amount')} USD has been processed. "
            f"Refund ID: {refund_result.get('refund_id')}"
        )

        try:
            self.notifier.send_notification(
                recipient=booking.booking_id,
                subject="Refund Confirmation",
                message=message,
                notification_type="REFUND",
            )
        except Exception:
            pass  # Silently fail if notification can't be sent
