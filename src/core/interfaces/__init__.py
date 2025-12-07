"""
Segregated interfaces for different system components.

ISP: Interface Segregation Principle - clients should not depend on interfaces they don't use.
Each interface is small and focused on specific capabilities.
"""

from .passenger_operations import PassengerOperations
from .staff_operations import StaffOperations
from .admin_operations import AdminOperations
from .payment_processor import PaymentProcessor
from .notifier import Notifier

__all__ = [
    "PassengerOperations",
    "StaffOperations",
    "AdminOperations",
    "PaymentProcessor",
    "Notifier",
]
