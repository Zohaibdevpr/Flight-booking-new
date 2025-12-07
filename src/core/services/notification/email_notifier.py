"""
Email notifier implementation.

DIP: Concrete implementation of the BaseNotifier for email notifications.
"""

import uuid
from .base_notifier import BaseNotifier


class EmailNotifier(BaseNotifier):
    """
    DIP: Email notification implementation.

    This implementation sends notifications via email while depending on
    the BaseNotifier abstraction.
    """

    def __init__(self, smtp_server: str = "smtp.example.com", port: int = 587):
        """
        Initialize email notifier.

        Args:
            smtp_server: SMTP server address
            port: SMTP port
        """
        super().__init__()
        self.smtp_server = smtp_server
        self.port = port

    def _send(self, recipient: str, subject: str, message: str) -> str:
        """
        Send email notification.

        Args:
            recipient: Email address
            subject: Email subject
            message: Email message

        Returns:
            Notification ID
        """
        # Validate email format
        if "@" not in recipient:
            raise ValueError(f"Invalid email address: {recipient}")

        # In a real implementation, this would connect to SMTP server
        # and send the email. For demo purposes, we'll just simulate it.

        notification_id = f"EMAIL-{str(uuid.uuid4())[:8].upper()}"

        # Simulate sending email
        print(f"[Email] Sending to {recipient}")
        print(f"  Subject: {subject}")
        print(f"  Message: {message}")

        return notification_id

    def get_channel_name(self) -> str:
        """Get channel name."""
        return "EMAIL"
