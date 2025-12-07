"""
Standard pricing strategy.

OCP: Concrete implementation of a flat pricing strategy.
"""

from .base_strategy import PricingStrategy


class StandardPricing(PricingStrategy):
    """
    OCP: Standard flat pricing strategy.

    This strategy applies a simple passenger type discount:
    - ADULT: 100% of base price
    - CHILD: 75% of base price
    - INFANT: Free (50% of base price for seat allocation)
    """

    def calculate_price(
        self,
        num_passengers: int,
        occupancy_rate: float,
        days_until_departure: int,
        passenger_type: str = "ADULT",
    ) -> float:
        """
        Calculate price using standard strategy.

        Args:
            num_passengers: Number of passengers
            occupancy_rate: Flight occupancy rate (unused in standard pricing)
            days_until_departure: Days until departure (unused in standard pricing)
            passenger_type: Type of passenger

        Returns:
            Calculated ticket price per passenger
        """
        self.validate_inputs(num_passengers, occupancy_rate, days_until_departure)

        # Apply passenger type discount
        multiplier = self._get_passenger_type_multiplier(passenger_type)
        return self.base_price * multiplier

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
        return "STANDARD"

    def get_strategy_description(self) -> str:
        """Get strategy description."""
        return "Flat pricing with passenger type discounts"
