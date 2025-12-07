"""
LSP (Liskov Substitution Principle) Demo

LSP states that objects of a superclass should be replaceable with objects of its subclasses
without breaking the application.

In this demo:
- CommercialAircraft and CargoPlanee are both Aircraft types
- Both can be used interchangeably wherever Aircraft is expected
- Each maintains the Aircraft contract
"""


def demo_lsp():
    """Demonstrate Liskov Substitution Principle."""
    from src.core.entities import CommercialAircraft, CargoPlanee

    print("\n" + "=" * 70)
    print("LSP: Liskov Substitution Principle Demo")
    print("=" * 70)

    print("\nBoth aircraft types are fully substitutable:\n")

    # Create CommercialAircraft
    commercial = CommercialAircraft(
        aircraft_id="B747-01",
        model="Boeing 747",
        manufacturer="Boeing",
        total_seats=300,
        first_class_seats=12,
        business_class_seats=48,
        economy_class_seats=240,
    )

    # Create CargoPlanee
    cargo = CargoPlanee(
        aircraft_id="B747F-01",
        model="Boeing 747F",
        manufacturer="Boeing",
        total_seats=0,
        cargo_capacity_kg=140000.0,
    )

    # Both are Aircraft - they're substitutable
    aircrafts = [commercial, cargo]

    for aircraft in aircrafts:
        print(f"[OK] Aircraft: {aircraft.model}")
        print(f"  Seat classes: {aircraft.get_seat_classes()}")
        print(f"  Luggage allowance: {aircraft.calculate_luggage_allowance()} kg")
        print(f"  Info: {aircraft.get_info()}")
        print()

    print("[OK] Both aircraft types satisfy the Aircraft contract!")
    print("\n[OK] LSP Demonstrated: Subtypes fully substitutable for base type!")


if __name__ == "__main__":
    demo_lsp() 
