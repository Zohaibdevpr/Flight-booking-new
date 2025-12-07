"""
Stripe payment gateway implementation.

DIP: Concrete implementation of PaymentGateway for Stripe.
"""

import uuid
from datetime import datetime
from .gateway_interface import PaymentGateway


class StripeGateway(PaymentGateway):
    """
    DIP: Stripe payment gateway implementation.

    This implementation handles Stripe payments while depending on
    the PaymentGateway abstraction.
    """

    def __init__(self, api_key: str = ""):
        """
        Initialize Stripe gateway.

        Args:
            api_key: Stripe API key
        """
        self.api_key = api_key
        self.transactions = {}

    def process_payment(
        self,
        transaction_id: str,
        amount: float,
        currency: str,
        customer_details: dict,
        payment_details: dict,
    ) -> dict:
        """
        Process payment via Stripe.

        Args:
            transaction_id: Unique transaction identifier
            amount: Payment amount
            currency: Currency code
            customer_details: Customer information
            payment_details: Card or payment details

        Returns:
            Result dictionary with transaction status
        """
        if amount <= 0:
            raise ValueError("Amount must be positive")

        # Validate payment details
        if "card_token" not in payment_details:
            raise ValueError("Card token is required for Stripe payment")

        # Simulate Stripe API call
        reference_id = f"STRIPE-{str(uuid.uuid4())[:16].upper()}"

        result = {
            "status": "SUCCESS",
            "reference_id": reference_id,
            "transaction_id": transaction_id,
            "amount": amount,
            "currency": currency,
            "gateway": "STRIPE",
            "timestamp": datetime.now().isoformat(),
        }

        # Store transaction
        self.transactions[reference_id] = result

        print(f"[Stripe] Processing payment: {amount} {currency}")
        print(f"  Transaction ID: {transaction_id}")
        print(f"  Reference ID: {reference_id}")

        return result

    def refund_payment(self, reference_id: str, amount: float, reason: str) -> dict:
        """
        Refund payment via Stripe.

        Args:
            reference_id: Original transaction reference ID
            amount: Refund amount
            reason: Reason for refund

        Returns:
            Result dictionary with refund status
        """
        if reference_id not in self.transactions:
            raise ValueError(f"Transaction not found: {reference_id}")

        if amount <= 0:
            raise ValueError("Refund amount must be positive")

        original_transaction = self.transactions[reference_id]

        if amount > original_transaction["amount"]:
            raise ValueError("Refund amount cannot exceed original amount")

        refund_id = f"REFUND-{str(uuid.uuid4())[:16].upper()}"

        result = {
            "status": "SUCCESS",
            "refund_id": refund_id,
            "original_reference": reference_id,
            "refund_amount": amount,
            "reason": reason,
            "gateway": "STRIPE",
            "timestamp": datetime.now().isoformat(),
        }

        print(f"[Stripe] Processing refund: {amount}")
        print(f"  Original Reference: {reference_id}")
        print(f"  Refund ID: {refund_id}")

        return result

    def verify_payment(self, reference_id: str) -> dict:
        """
        Verify payment via Stripe.

        Args:
            reference_id: Transaction reference ID

        Returns:
            Result dictionary with payment status
        """
        if reference_id not in self.transactions:
            return {"status": "NOT_FOUND", "reference_id": reference_id}

        transaction = self.transactions[reference_id]

        return {
            "status": "CONFIRMED",
            "reference_id": reference_id,
            "amount": transaction["amount"],
            "currency": transaction["currency"],
            "gateway": "STRIPE",
        }

    def get_gateway_name(self) -> str:
        """Get gateway name."""
        return "STRIPE"
