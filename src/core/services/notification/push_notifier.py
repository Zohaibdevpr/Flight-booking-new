"""
Push notification implementation.

DIP: Concrete implementation of the BaseNotifier for push notifications.
"""

import uuid
from .base_notifier import BaseNotifier


class PushNotifier(BaseNotifier):
    """
    DIP: Push notification implementation.

    This implementation sends notifications via push while depending on
    the BaseNotifier abstraction.
    """

    def __init__(self, api_key: str = ""):
        """
        Initialize push notifier.

        Args:
            api_key: API key for push notification service
        """
        super().__init__()
        self.api_key = api_key

    def _send(self, recipient: str, subject: str, message: str) -> str:
        """
        Send push notification.

        Args:
            recipient: User ID or device ID
            subject: Notification title
            message: Notification message

        Returns:
            Notification ID
        """
        if not recipient:
            raise ValueError("Recipient (user/device ID) is required")

        # In a real implementation, this would call push notification service
        # For demo purposes, we'll just simulate it.

        notification_id = f"PUSH-{str(uuid.uuid4())[:8].upper()}"

        # Simulate sending push notification
        print(f"[Push] Sending to {recipient}")
        print(f"  Title: {subject}")
        print(f"  Message: {message}")

        return notification_id

    def get_channel_name(self) -> str:
        """Get channel name."""
        return "PUSH"
