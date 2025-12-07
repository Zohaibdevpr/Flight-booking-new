"""
OCP (Open/Closed Principle) Demo

OCP states that software should be open for extension but closed for modification.
You can add new functionality without changing existing code.

In this demo:
- New pricing strategies can be added without modifying existing BookingService
- New seating strategies can be added without modifying existing BookingService
"""


def demo_ocp():
    """Demonstrate Open/Closed Principle."""
    from datetime import datetime, timedelta
    from src.core.entities import Flight, FlightStatus
    from src.core.services.pricing import (
        StandardPricing,
        DynamicPricing,
        SeasonalPricing,
        LoyaltyPricing,
    )
    from src.core.services.seating import (
        SequentialAllocation,
        WindowPriority,
        FamilyAllocation,
    )
    from src.utils import format_currency

    print("\n" + "=" * 70)
    print("OCP: Open/Closed Principle Demo")
    print("=" * 70)

    # Part 1: Pricing Strategies
    print("\n1. PRICING STRATEGIES (OCP in action)")
    print("-" * 70)

    base_price = 100.0
    num_passengers = 2
    occupancy_rate = 75.0
    days_to_departure = 10

    # Different strategies WITHOUT modifying code
    strategies = [
        StandardPricing(base_price),
        DynamicPricing(base_price),
        SeasonalPricing(base_price),
        LoyaltyPricing(base_price),
    ]

    print(f"\nBase price: {format_currency(base_price)}")
    print(f"Scenario: {num_passengers} passengers, {occupancy_rate}% occupancy, {days_to_departure} days to departure\n")

    for strategy in strategies:
        if isinstance(strategy, SeasonalPricing):
            price = strategy.calculate_price(
                num_passengers, occupancy_rate, days_to_departure, "ADULT", departure_month=7
            )
        elif isinstance(strategy, LoyaltyPricing):
            price = strategy.calculate_price(
                num_passengers, occupancy_rate, days_to_departure, "ADULT", loyalty_tier="GOLD"
            )
        else:
            price = strategy.calculate_price(
                num_passengers, occupancy_rate, days_to_departure, "ADULT"
            )

        total = price * num_passengers
        strategy_name = strategy.get_strategy_name()
        print(f"[OK] {strategy_name}: {format_currency(price)}/person = {format_currency(total)} total")

    print("\n[OK] New pricing strategies can be added WITHOUT modifying existing code!")

    # Part 2: Seating Strategies
    print("\n2. SEATING STRATEGIES (OCP in action)")
    print("-" * 70)

    available_seats = ["1A", "1B", "1C", "1D", "1E", "1F",
                      "2A", "2B", "2C", "2D", "2E", "2F"]

    print(f"\nAvailable seats: {available_seats}")
    print("Allocating 4 seats for passengers using different strategies:\n")

    # Sequential Allocation
    seq_strategy = SequentialAllocation(available_seats.copy())
    seq_seats = seq_strategy.allocate_seats(4)
    print(f"[OK] Sequential: {seq_seats}")

    # Window Priority
    window_strategy = WindowPriority(available_seats.copy())
    window_seats = window_strategy.allocate_seats(4)
    print(f"[OK] Window Priority: {window_seats}")

    # Family Allocation
    family_strategy = FamilyAllocation(available_seats.copy())
    family_seats = family_strategy.allocate_seats(4)
    print(f"[OK] Family Allocation: {family_seats}")

    print("\n[OK] New seating strategies can be added WITHOUT modifying existing code!")

    print("\n[OK] OCP Demonstrated: Add features by extending, not modifying!")


if __name__ == "__main__":
    demo_ocp() 
