"""
Notifier interface.

ISP: This interface defines the contract for sending notifications.
Different notification channels (email, SMS, push) implement this interface.
"""

from abc import ABC, abstractmethod
from typing import Optional, List


class Notifier(ABC):
    """
    ISP: Interface for sending notifications.

    Notifiers must:
    - Send notifications
    - Support different message types
    - Track notification status
    """

    @abstractmethod
    def send_notification(
        self,
        recipient: str,
        subject: str,
        message: str,
        notification_type: str = "standard",
    ) -> dict:
        """
        Send a notification to a recipient.

        Args:
            recipient: Recipient identifier (email, phone, user ID, etc.)
            subject: Notification subject
            message: Notification message
            notification_type: Type of notification (BOOKING, PAYMENT, CHECK_IN, etc.)

        Returns:
            Result dictionary with notification ID and status
        """
        pass

    @abstractmethod
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
            Result dictionary with batch ID and status
        """
        pass

    @abstractmethod
    def get_notification_status(self, notification_id: str) -> str:
        """
        Get the status of a sent notification.

        Args:
            notification_id: Notification identifier

        Returns:
            Notification status (SENT, DELIVERED, FAILED, etc.)
        """
        pass
