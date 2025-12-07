"""
Pricing strategies for the flight booking system.

OCP: Open/Closed Principle - The system is open for extension (new pricing strategies)
but closed for modification (existing strategies don't need to change).
"""

from .base_strategy import PricingStrategy
from .standard_pricing import StandardPricing
from .dynamic_pricing import DynamicPricing
from .seasonal_pricing import SeasonalPricing
from .loyalty_pricing import LoyaltyPricing

__all__ = [
    "PricingStrategy",
    "StandardPricing",
    "DynamicPricing",
    "SeasonalPricing",
    "LoyaltyPricing",
]
