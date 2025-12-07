"""
Dynamic pricing strategy.

OCP: Concrete implementation of a dynamic pricing strategy.
Prices change based on demand (occupancy rate) and time to departure.
"""

from .base_strategy import PricingStrategy


class DynamicPricing(PricingStrategy):
    """
    OCP: Dynamic pricing strategy.

    This strategy adjusts prices based on:
    - Occupancy rate (higher occupancy = higher price)
    - Time to departure (closer to departure = higher price)

    Formula:
    - Occupancy multiplier: 1.0 + (occupancy_rate / 100) * 0.5
    - Time multiplier: 1.0 + (100 / (days_until_departure + 1)) * 0.25
    - Final price = base_price * occupancy_multiplier * time_multiplier
    """

    MIN_OCCUPANCY_MULTIPLIER = 1.0
    MAX_OCCUPANCY_MULTIPLIER = 1.5
    TIME_MULTIPLIER_FACTOR = 0.25

    def calculate_price(
        self,
        num_passengers: int,
        occupancy_rate: float,
        days_until_departure: int,
        passenger_type: str = "ADULT",
    ) -> float:
        """
        Calculate price using dynamic strategy.

        Args:
            num_passengers: Number of passengers
            occupancy_rate: Flight occupancy rate (0-100)
            days_until_departure: Days until departure
            passenger_type: Type of passenger

        Returns:
            Calculated ticket price per passenger
        """
        self.validate_inputs(num_passengers, occupancy_rate, days_until_departure)

        # Calculate occupancy-based multiplier
        occupancy_multiplier = self._calculate_occupancy_multiplier(occupancy_rate)

        # Calculate time-based multiplier
        time_multiplier = self._calculate_time_multiplier(days_until_departure)

        # Apply passenger type discount
        passenger_multiplier = self._get_passenger_type_multiplier(passenger_type)

        # Calculate final price
        final_price = (
            self.base_price * occupancy_multiplier * time_multiplier * passenger_multiplier
        )

        return round(final_price, 2)

    def _calculate_occupancy_multiplier(self, occupancy_rate: float) -> float:
        """
        Calculate occupancy-based price multiplier.

        Args:
            occupancy_rate: Flight occupancy rate (0-100)

        Returns:
            Occupancy multiplier
        """
        # Higher occupancy = higher price
        # At 0% occupancy: 1.0x, At 100% occupancy: 1.5x
        return 1.0 + (occupancy_rate / 100) * 0.5

    def _calculate_time_multiplier(self, days_until_departure: int) -> float:
        """
        Calculate time-based price multiplier.

        Args:
            days_until_departure: Days until departure

        Returns:
            Time multiplier
        """
        # Closer to departure = higher price
        # At 100 days: ~1.0x, At 0 days: ~26x
        if days_until_departure == 0:
            days_until_departure = 1

        return 1.0 + (100 / (days_until_departure + 1)) * self.TIME_MULTIPLIER_FACTOR

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
        return "DYNAMIC"

    def get_strategy_description(self) -> str:
        """Get strategy description."""
        return "Dynamic pricing based on occupancy and time to departure"
