"""
PayPal payment gateway implementation.

DIP: Concrete implementation of PaymentGateway for PayPal.
"""

import uuid
from datetime import datetime
from .gateway_interface import PaymentGateway


class PayPalGateway(PaymentGateway):
    """
    DIP: PayPal payment gateway implementation.

    This implementation handles PayPal payments while depending on
    the PaymentGateway abstraction.
    """

    def __init__(self, client_id: str = "", client_secret: str = ""):
        """
        Initialize PayPal gateway.

        Args:
            client_id: PayPal client ID
            client_secret: PayPal client secret
        """
        self.client_id = client_id
        self.client_secret = client_secret
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
        Process payment via PayPal.

        Args:
            transaction_id: Unique transaction identifier
            amount: Payment amount
            currency: Currency code
            customer_details: Customer information
            payment_details: PayPal account or token details

        Returns:
            Result dictionary with transaction status
        """
        if amount <= 0:
            raise ValueError("Amount must be positive")

        # Validate payment details
        if "paypal_account" not in payment_details:
            raise ValueError("PayPal account is required")

        # Simulate PayPal API call
        reference_id = f"PAYPAL-{str(uuid.uuid4())[:16].upper()}"

        result = {
            "status": "SUCCESS",
            "reference_id": reference_id,
            "transaction_id": transaction_id,
            "amount": amount,
            "currency": currency,
            "gateway": "PAYPAL",
            "timestamp": datetime.now().isoformat(),
        }

        # Store transaction
        self.transactions[reference_id] = result

        print(f"[PayPal] Processing payment: {amount} {currency}")
        print(f"  Transaction ID: {transaction_id}")
        print(f"  Reference ID: {reference_id}")

        return result

    def refund_payment(self, reference_id: str, amount: float, reason: str) -> dict:
        """
        Refund payment via PayPal.

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
            "gateway": "PAYPAL",
            "timestamp": datetime.now().isoformat(),
        }

        print(f"[PayPal] Processing refund: {amount}")
        print(f"  Original Reference: {reference_id}")
        print(f"  Refund ID: {refund_id}")

        return result

    def verify_payment(self, reference_id: str) -> dict:
        """
        Verify payment via PayPal.

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
            "gateway": "PAYPAL",
        }

    def get_gateway_name(self) -> str:
        """Get gateway name."""
        return "PAYPAL"
