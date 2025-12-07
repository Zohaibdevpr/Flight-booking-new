"""
Credit card payment gateway implementation.

DIP: Concrete implementation of PaymentGateway for direct credit card processing.
"""

import uuid
from datetime import datetime
from .gateway_interface import PaymentGateway


class CreditCardGateway(PaymentGateway):
    """
    DIP: Credit card payment gateway implementation.

    This implementation handles direct credit card payments while depending on
    the PaymentGateway abstraction.
    """

    def __init__(self, merchant_id: str = ""):
        """
        Initialize credit card gateway.

        Args:
            merchant_id: Merchant ID for credit card processing
        """
        self.merchant_id = merchant_id
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
        Process payment via credit card.

        Args:
            transaction_id: Unique transaction identifier
            amount: Payment amount
            currency: Currency code
            customer_details: Customer information
            payment_details: Credit card details

        Returns:
            Result dictionary with transaction status
        """
        if amount <= 0:
            raise ValueError("Amount must be positive")

        # Validate credit card details
        required_fields = ["card_number", "cvv", "expiry_date"]
        for field in required_fields:
            if field not in payment_details:
                raise ValueError(f"Credit card field '{field}' is required")

        # Validate card number (simplified - just check length)
        card_number = str(payment_details["card_number"])
        if len(card_number) < 13 or len(card_number) > 19:
            raise ValueError("Invalid card number length")

        # Simulate credit card processing
        reference_id = f"CC-{str(uuid.uuid4())[:16].upper()}"

        result = {
            "status": "SUCCESS",
            "reference_id": reference_id,
            "transaction_id": transaction_id,
            "amount": amount,
            "currency": currency,
            "gateway": "CREDIT_CARD",
            "last_four_digits": card_number[-4:],
            "timestamp": datetime.now().isoformat(),
        }

        # Store transaction
        self.transactions[reference_id] = result

        print(f"[Credit Card] Processing payment: {amount} {currency}")
        print(f"  Transaction ID: {transaction_id}")
        print(f"  Reference ID: {reference_id}")
        print(f"  Card ending in: {card_number[-4:]}")

        return result

    def refund_payment(self, reference_id: str, amount: float, reason: str) -> dict:
        """
        Refund payment via credit card.

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
            "gateway": "CREDIT_CARD",
            "timestamp": datetime.now().isoformat(),
        }

        print(f"[Credit Card] Processing refund: {amount}")
        print(f"  Original Reference: {reference_id}")
        print(f"  Refund ID: {refund_id}")

        return result

    def verify_payment(self, reference_id: str) -> dict:
        """
        Verify payment via credit card.

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
            "gateway": "CREDIT_CARD",
            "last_four_digits": transaction.get("last_four_digits"),
        }

    def get_gateway_name(self) -> str:
        """Get gateway name."""
        return "CREDIT_CARD"
