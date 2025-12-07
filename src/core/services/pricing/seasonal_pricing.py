"""
Seasonal pricing strategy.

OCP: Concrete implementation of a seasonal pricing strategy.
Prices vary based on the season (peak vs off-season).
"""

from .base_strategy import PricingStrategy


class SeasonalPricing(PricingStrategy):
    """
    OCP: Seasonal pricing strategy.

    This strategy applies seasonal multipliers:
    - Peak season (Dec, Jan, Jul, Aug): 1.3x base price
    - High season (Mar-May, Jun, Sep-Oct): 1.15x base price
    - Low season (Feb): 0.85x base price
    """

    # Seasonal multipliers for each month (1-12)
    SEASONAL_MULTIPLIERS = {
        1: 1.3,   # January - Peak
        2: 0.85,  # February - Low
        3: 1.15,  # March - High
        4: 1.15,  # April - High
        5: 1.15,  # May - High
        6: 1.15,  # June - High
        7: 1.3,   # July - Peak
        8: 1.3,   # August - Peak
        9: 1.15,  # September - High
        10: 1.15, # October - High
        11: 1.0,  # November - Standard
        12: 1.3,  # December - Peak
    }

    def calculate_price(
        self,
        num_passengers: int,
        occupancy_rate: float,
        days_until_departure: int,
        passenger_type: str = "ADULT",
        departure_month: int = None,
    ) -> float:
        """
        Calculate price using seasonal strategy.

        Args:
            num_passengers: Number of passengers
            occupancy_rate: Flight occupancy rate (unused in seasonal pricing)
            days_until_departure: Days until departure (unused)
            passenger_type: Type of passenger
            departure_month: Month of departure (1-12, required for seasonal pricing)

        Returns:
            Calculated ticket price per passenger
        """
        self.validate_inputs(num_passengers, occupancy_rate, days_until_departure)

        if departure_month is None or not (1 <= departure_month <= 12):
            raise ValueError("Valid departure_month (1-12) is required for seasonal pricing")

        # Get seasonal multiplier
        seasonal_multiplier = self.SEASONAL_MULTIPLIERS.get(departure_month, 1.0)

        # Apply passenger type discount
        passenger_multiplier = self._get_passenger_type_multiplier(passenger_type)

        # Calculate final price
        final_price = self.base_price * seasonal_multiplier * passenger_multiplier

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
        return "SEASONAL"

    def get_strategy_description(self) -> str:
        """Get strategy description."""
        return "Seasonal pricing with peak, high, and low season rates"
