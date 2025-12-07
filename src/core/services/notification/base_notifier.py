"""
Base notifier abstract class.

DIP: Abstract base class for all notification types.
Different notification channels depend on this abstraction.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
import uuid


class BaseNotifier(ABC):
    """
    DIP: Abstract base class for all notifiers.

    High-level modules depend on this interface, not on specific notification implementations.
    """

    def __init__(self):
        """Initialize notifier."""
        self.notifications_sent = 0

    @abstractmethod
    def _send(self, recipient: str, subject: str, message: str) -> str:
        """
        Send notification through specific channel.

        Args:
            recipient: Recipient identifier
            subject: Notification subject
            message: Notification message

        Returns:
            Notification ID
        """
        pass

    def send_notification(
        self,
        recipient: str,
        subject: str,
        message: str,
        notification_type: str = "standard",
    ) -> dict:
        """
        Send a notification.

        Args:
            recipient: Recipient identifier
            subject: Notification subject
            message: Notification message
            notification_type: Type of notification

        Returns:
            Result dictionary with notification details
        """
        if not recipient or not subject or not message:
            raise ValueError("Recipient, subject, and message are required")

        notification_id = self._send(recipient, subject, message)
        self.notifications_sent += 1

        return {
            "notification_id": notification_id,
            "status": "SENT",
            "timestamp": datetime.now().isoformat(),
            "channel": self.get_channel_name(),
            "recipient": recipient,
            "type": notification_type,
        }

    def send_bulk_notification(
        self,
        recipients: List[str],
        subject: str,
        message: str,
        notification_type: str = "standard",
    ) -> dict:
        """
        Send notifications to multiple recipients.

        Args:
            recipients: List of recipient identifiers
            subject: Notification subject
            message: Notification message
            notification_type: Type of notification

        Returns:
            Result dictionary with batch details
        """
        if not recipients:
            raise ValueError("At least one recipient is required")

        batch_id = str(uuid.uuid4())
        sent_count = 0

        for recipient in recipients:
            try:
                self.send_notification(recipient, subject, message, notification_type)
                sent_count += 1
            except Exception:
                pass  # Continue with next recipient

        return {
            "batch_id": batch_id,
            "status": "COMPLETED",
            "total_recipients": len(recipients),
            "successfully_sent": sent_count,
            "failed": len(recipients) - sent_count,
            "timestamp": datetime.now().isoformat(),
            "channel": self.get_channel_name(),
        }

    def get_notification_status(self, notification_id: str) -> str:
        """
        Get notification status.

        Args:
            notification_id: Notification identifier

        Returns:
            Notification status
        """
        # Simplified implementation - in real system, would check against database
        return "DELIVERED"

    @abstractmethod
    def get_channel_name(self) -> str:
        """
        Get the name of the notification channel.

        Returns:
            Channel name
        """
        pass
