"""
Payment gateway abstraction module.

DIP: Dependency Inversion Principle - High-level modules depend on payment gateway abstraction,
not concrete payment provider implementations.
"""

from .gateway_interface import PaymentGateway
from .stripe_gateway import StripeGateway
from .paypal_gateway import PayPalGateway
from .credit_card_gateway import CreditCardGateway

__all__ = [
    "PaymentGateway",
    "StripeGateway",
    "PayPalGateway",
    "CreditCardGateway",
]
