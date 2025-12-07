"""
Base pricing strategy class.

OCP: Abstract base class that defines the pricing contract.
All pricing strategies must inherit from this class and implement calculate_price method.
"""

from abc import ABC, abstractmethod
from typing import Optional


class PricingStrategy(ABC):
    """
    OCP: Abstract base class for all pricing strategies.

    This class defines the contract that all pricing strategies must follow.
    New pricing strategies can be added without modifying existing code.
    """

    def __init__(self, base_price: float):
        """
        Initialize pricing strategy.

        Args:
            base_price: Base ticket price
        """
        if base_price < 0:
            raise ValueError("Base price cannot be negative")
        self.base_price = base_price

    @abstractmethod
    def calculate_price(
        self,
        num_passengers: int,
        occupancy_rate: float,
        days_until_departure: int,
        passenger_type: str = "ADULT",
    ) -> float:
        """
        Calculate ticket price based on strategy.

        Args:
            num_passengers: Number of passengers
            occupancy_rate: Flight occupancy rate (0-100)
            days_until_departure: Days until flight departure
            passenger_type: Type of passenger (ADULT, CHILD, INFANT)

        Returns:
            Calculated ticket price per passenger
        """
        pass

    @abstractmethod
    def get_strategy_name(self) -> str:
        """
        Get the name of this pricing strategy.

        Returns:
            Strategy name
        """
        pass

    @abstractmethod
    def get_strategy_description(self) -> str:
        """
        Get description of this pricing strategy.

        Returns:
            Strategy description
        """
        pass

    def validate_inputs(
        self,
        num_passengers: int,
        occupancy_rate: float,
        days_until_departure: int,
    ) -> None:
        """
        Validate input parameters.

        Args:
            num_passengers: Number of passengers
            occupancy_rate: Flight occupancy rate
            days_until_departure: Days until departure

        Raises:
            ValueError: If inputs are invalid
        """
        if num_passengers <= 0:
            raise ValueError("Number of passengers must be positive")
        if not (0 <= occupancy_rate <= 100):
            raise ValueError("Occupancy rate must be between 0 and 100")
        if days_until_departure < 0:
            raise ValueError("Days until departure cannot be negative")
