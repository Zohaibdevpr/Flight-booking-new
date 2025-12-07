"""
Loyalty pricing strategy.

OCP: Concrete implementation of a loyalty-based pricing strategy.
Regular customers receive discounts based on loyalty tier.
"""

from .base_strategy import PricingStrategy
from enum import Enum


class LoyaltyTier(Enum):
    """Loyalty tier enumeration."""

    BRONZE = "BRONZE"
    SILVER = "SILVER"
    GOLD = "GOLD"
    PLATINUM = "PLATINUM"


class LoyaltyPricing(PricingStrategy):
    """
    OCP: Loyalty pricing strategy.

    This strategy applies discounts based on loyalty tier:
    - BRONZE: 0% discount
    - SILVER: 5% discount (10+ flights)
    - GOLD: 10% discount (50+ flights)
    - PLATINUM: 15% discount (100+ flights)
    """

    LOYALTY_DISCOUNTS = {
        LoyaltyTier.BRONZE: 0.0,
        LoyaltyTier.SILVER: 0.05,
        LoyaltyTier.GOLD: 0.10,
        LoyaltyTier.PLATINUM: 0.15,
    }

    def calculate_price(
        self,
        num_passengers: int,
        occupancy_rate: float,
        days_until_departure: int,
        passenger_type: str = "ADULT",
        loyalty_tier: str = None,
    ) -> float:
        """
        Calculate price using loyalty strategy.

        Args:
            num_passengers: Number of passengers
            occupancy_rate: Flight occupancy rate (unused)
            days_until_departure: Days until departure (unused)
            passenger_type: Type of passenger
            loyalty_tier: Loyalty tier (BRONZE, SILVER, GOLD, PLATINUM)

        Returns:
            Calculated ticket price per passenger
        """
        self.validate_inputs(num_passengers, occupancy_rate, days_until_departure)

        # Default to BRONZE tier if not specified
        if loyalty_tier is None:
            loyalty_tier = LoyaltyTier.BRONZE
        elif isinstance(loyalty_tier, str):
            try:
                loyalty_tier = LoyaltyTier[loyalty_tier.upper()]
            except KeyError:
                loyalty_tier = LoyaltyTier.BRONZE

        # Get loyalty discount
        discount_rate = self.LOYALTY_DISCOUNTS.get(loyalty_tier, 0.0)

        # Apply passenger type discount
        passenger_multiplier = self._get_passenger_type_multiplier(passenger_type)

        # Calculate final price with loyalty discount
        base_final_price = self.base_price * passenger_multiplier
        final_price = base_final_price * (1 - discount_rate)

        return round(final_price, 2)

    def _get_passenger_type_multiplier(self, passenger_type: str) -> float:
        """
        Get price multiplier for passenger type.

        Args:
            passenger_type: Type of passenger

        Returns:
            Price multiplier
        """
        multipliers = {
            "ADULT": 1.0,
            "CHILD": 0.75,
            "INFANT": 0.5,
        }
        return multipliers.get(passenger_type, 1.0)

    def get_strategy_name(self) -> str:
        """Get strategy name."""
        return "LOYALTY"

    def get_strategy_description(self) -> str:
        """Get strategy description."""
        return "Loyalty-based pricing with tier-dependent discounts"

    @staticmethod
    def get_loyalty_discount(loyalty_tier: str) -> float:
        """
        Get discount rate for a loyalty tier.

        Args:
            loyalty_tier: Loyalty tier name

        Returns:
            Discount rate (0-1)
        """
        try:
            tier = LoyaltyTier[loyalty_tier.upper()]
            return LoyaltyPricing.LOYALTY_DISCOUNTS.get(tier, 0.0)
        except KeyError:
            return 0.0
