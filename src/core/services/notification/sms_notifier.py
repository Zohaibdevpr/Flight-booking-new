"""
SMS notifier implementation.

DIP: Concrete implementation of the BaseNotifier for SMS notifications.
"""

import uuid
from .base_notifier import BaseNotifier


class SMSNotifier(BaseNotifier):
    """
    DIP: SMS notification implementation.

    This implementation sends notifications via SMS while depending on
    the BaseNotifier abstraction.
    """

    def __init__(self, api_key: str = ""):
        """
        Initialize SMS notifier.

        Args:
            api_key: API key for SMS service provider
        """
        super().__init__()
        self.api_key = api_key

    def _send(self, recipient: str, subject: str, message: str) -> str:
        """
        Send SMS notification.

        Args:
            recipient: Phone number
            subject: SMS subject (not used for SMS, included for interface compatibility)
            message: SMS message

        Returns:
            Notification ID
        """
        # Validate phone number format
        digits = "".join(c for c in recipient if c.isdigit())
        if len(digits) < 10:
            raise ValueError(f"Invalid phone number: {recipient}")

        # In a real implementation, this would call SMS API provider
        # For demo purposes, we'll just simulate it.

        notification_id = f"SMS-{str(uuid.uuid4())[:8].upper()}"

        # Simulate sending SMS
        print(f"[SMS] Sending to {recipient}")
        print(f"  Message: {message}")

        return notification_id

    def get_channel_name(self) -> str:
        """Get channel name."""
        return "SMS"
