"""
Flight Booking System - Main Entry Point

This is the main entry point for the complete Flight Booking System
demonstrating all SOLID principles in Python.

SOLID Principles Demonstrated:
1. SRP (Single Responsibility Principle): Each class has one responsibility
2. OCP (Open/Closed Principle): System is open for extension (new strategies) but closed for modification
3. LSP (Liskov Substitution Principle): Aircraft types are fully substitutable
4. ISP (Interface Segregation Principle): Small, focused interfaces for different roles
5. DIP (Dependency Inversion Principle): High-level modules depend on abstractions

Usage:
    python main.py
"""

from datetime import datetime, timedelta
from src.core.entities import (
    Flight,
    FlightStatus,
    Passenger,
    PassengerType,
    CommercialAircraft,
)
from src.core.services import FlightService, BookingService, PaymentService
from src.core.services.pricing import (
    StandardPricing,
    DynamicPricing,
    SeasonalPricing,
    LoyaltyPricing,
)
from src.core.services.seating import SequentialAllocation
from src.core.services.notification import EmailNotifier, SMSNotifier, PushNotifier
from src.core.repositories import InMemoryRepository
from src.payment import StripeGateway, PayPalGateway, CreditCardGateway
from src.utils import validate_email, format_currency


def create_sample_flights() -> tuple:
    """Create sample flights for demonstration."""
    flights = []

    # Flight 1: NYC to LA
    flight1 = Flight(
        flight_number="AA101",
        origin="New York",
        destination="Los Angeles",
        departure_time=datetime.now() + timedelta(days=5),
        arrival_time=datetime.now() + timedelta(days=5, hours=6),
        aircraft_id="AC001",
        total_seats=300,
        available_seats=50,
        status=FlightStatus.SCHEDULED,
        price=250.0,
    )
    flights.append(flight1)

    # Flight 2: LA to NYC
    flight2 = Flight(
        flight_number="AA102",
        origin="Los Angeles",
        destination="New York",
        departure_time=datetime.now() + timedelta(days=7),
        arrival_time=datetime.now() + timedelta(days=7, hours=5),
        aircraft_id="AC002",
        total_seats=300,
        available_seats=120,
        status=FlightStatus.SCHEDULED,
        price=280.0,
    )
    flights.append(flight2)

    # Flight 3: NYC to London
    flight3 = Flight(
        flight_number="BA501",
        origin="New York",
        destination="London",
        departure_time=datetime.now() + timedelta(days=10),
        arrival_time=datetime.now() + timedelta(days=10, hours=8),
        aircraft_id="AC003",
        total_seats=400,
        available_seats=80,
        status=FlightStatus.SCHEDULED,
        price=450.0,
    )
    flights.append(flight3)

    return tuple(flights)


def create_sample_passengers() -> tuple:
    """Create sample passengers for demonstration."""
    passengers = []

    # Passenger 1: Adult
    passenger1 = Passenger(
        passenger_id="P001",
        first_name="John",
        last_name="Smith",
        email="john.smith@example.com",
        phone="+1-212-555-0123",
        date_of_birth="1990-01-15",
        passenger_type=PassengerType.ADULT,
        loyalty_number="LOY001",
    )
    passengers.append(passenger1)

    # Passenger 2: Adult
    passenger2 = Passenger(
        passenger_id="P002",
        first_name="Jane",
        last_name="Doe",
        email="jane.doe@example.com",
        phone="+1-212-555-0124",
        date_of_birth="1985-05-20",
        passenger_type=PassengerType.ADULT,
        loyalty_number="LOY002",
    )
    passengers.append(passenger2)

    # Passenger 3: Child
    passenger3 = Passenger(
        passenger_id="P003",
        first_name="Tommy",
        last_name="Smith",
        email="tommy.smith@example.com",
        phone="+1-212-555-0125",
        date_of_birth="2010-08-10",
        passenger_type=PassengerType.CHILD,
    )
    passengers.append(passenger3)

    return tuple(passengers)


def demo_srp_solid_principle():
    """
    SRP: Single Responsibility Principle

    Each class has a single, well-defined responsibility:
    - Flight: Represents flight data and seat management
    - Passenger: Represents passenger profile
    - Booking: Represents booking and booking lifecycle
    """
    print("\n" + "=" * 70)
    print("DEMO 1: SRP - Single Responsibility Principle")
    print("=" * 70)

    flights = create_sample_flights()
    passengers = create_sample_passengers()

    print("\n✓ Flight entity - Responsible for flight data and seat management:")
    print(f"  Flight: {flights[0].flight_number}")
    print(f"  Route: {flights[0].origin} → {flights[0].destination}")
    print(f"  Available seats: {flights[0].available_seats}/{flights[0].total_seats}")
    print(f"  Occupancy rate: {flights[0].get_occupancy_rate():.1f}%")

    print("\n✓ Passenger entity - Responsible for passenger profile:")
    print(f"  Passenger: {passengers[0].full_name}")
    print(f"  Email: {passengers[0].email}")
    print(f"  Profile: {passengers[0].get_profile()}")

    print("\n✓ Each class has ONE responsibility - no mixing concerns!")


def demo_ocp_pricing_strategies():
    """
    OCP: Open/Closed Principle

    The system is OPEN for extension (new pricing strategies can be added)
    but CLOSED for modification (existing strategies don't change).

    New pricing strategies can be created by simply implementing PricingStrategy.
    """
    print("\n" + "=" * 70)
    print("DEMO 2: OCP - Open/Closed Principle (Pricing Strategies)")
    print("=" * 70)

    base_price = 100.0
    num_passengers = 2
    occupancy_rate = 75.0
    days_to_departure = 10

    # Use different pricing strategies WITHOUT modifying existing code
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
        print(f"✓ {strategy.get_strategy_name()}: {format_currency(price)}/person = {format_currency(total)} total")
        print(f"  ({strategy.get_strategy_description()})")

    print("\n✓ New pricing strategies can be added WITHOUT modifying existing code!")


def demo_ocp_seating_strategies():
    """
    OCP: Open/Closed Principle (Seating Strategies)

    Similar to pricing, seating strategies demonstrate OCP.
    New seating strategies can be added without modifying existing code.
    """
    print("\n" + "=" * 70)
    print("DEMO 3: OCP - Open/Closed Principle (Seating Strategies)")
    print("=" * 70)

    # Available seats: A (window), B, C, D, E (window for 6-seat config)
    available_seats = ["1A", "1B", "1C", "1D", "1E", "1F",
                      "2A", "2B", "2C", "2D", "2E", "2F"]

    print(f"\nAvailable seats: {available_seats}")
    print("Allocating 4 seats for passengers using different strategies:\n")

    # Sequential Allocation
    seq_strategy = SequentialAllocation(available_seats.copy())
    seq_seats = seq_strategy.allocate_seats(4)
    print(f"✓ Sequential: {seq_seats}")

    # Window Priority
    from src.core.services.seating import WindowPriority
    window_strategy = WindowPriority(available_seats.copy())
    window_seats = window_strategy.allocate_seats(4)
    print(f"✓ Window Priority: {window_seats}")

    # Family Allocation
    from src.core.services.seating import FamilyAllocation
    family_strategy = FamilyAllocation(available_seats.copy())
    family_seats = family_strategy.allocate_seats(4)
    print(f"✓ Family Allocation: {family_seats}")

    print("\n✓ New seating strategies can be added WITHOUT modifying existing code!")


def demo_lsp_aircraft_substitution():
    """
    LSP: Liskov Substitution Principle

    Different aircraft types (CommercialAircraft, CargoPlanee) can be used
    interchangeably wherever Aircraft is expected.
    All aircraft types maintain the same contract.
    """
    print("\n" + "=" * 70)
    print("DEMO 4: LSP - Liskov Substitution Principle (Aircraft Hierarchy)")
    print("=" * 70)

    # Create different aircraft types
    commercial = CommercialAircraft(
        aircraft_id="B747-01",
        model="Boeing 747",
        manufacturer="Boeing",
        total_seats=300,
        first_class_seats=12,
        business_class_seats=48,
        economy_class_seats=240,
    )

    from src.core.entities import CargoPlanee
    cargo = CargoPlanee(
        aircraft_id="B747F-01",
        model="Boeing 747F",
        manufacturer="Boeing",
        total_seats=0,
        cargo_capacity_kg=140000.0,
    )

    # Both aircraft types are substitutable - they implement the same interface
    aircrafts = [commercial, cargo]

    print("\nAll aircraft types implement the same contract (are fully substitutable):\n")

    for aircraft in aircrafts:
        print(f"✓ Aircraft: {aircraft.model}")
        print(f"  Seat classes: {aircraft.get_seat_classes()}")
        print(f"  Luggage allowance: {aircraft.calculate_luggage_allowance()} kg")
        print(f"  Info: {aircraft.get_info()}")
        print()

    print("✓ Both aircraft types satisfy the Aircraft contract!")


def demo_isp_segregated_interfaces():
    """
    ISP: Interface Segregation Principle

    Instead of large interfaces that clients don't fully use,
    we have small, focused interfaces for specific roles.
    """
    print("\n" + "=" * 70)
    print("DEMO 5: ISP - Interface Segregation Principle")
    print("=" * 70)

    print("\n✓ Segregated interfaces for different roles:\n")

    print("  PassengerOperations:")
    print("    - search_flights()")
    print("    - make_booking()")
    print("    - view_my_bookings()")
    print("    - cancel_booking()")
    print("    - check_booking_status()")

    print("\n  StaffOperations:")
    print("    - check_flight_status()")
    print("    - get_passenger_list()")
    print("    - process_check_in()")
    print("    - generate_boarding_pass()")
    print("    - handle_cancellation_request()")

    print("\n  AdminOperations:")
    print("    - add_flight()")
    print("    - add_aircraft()")
    print("    - set_pricing_strategy()")
    print("    - get_revenue_report()")
    print("    - get_system_statistics()")

    print("\n✓ PaymentProcessor interface (small, focused):")
    print("    - process_payment()")
    print("    - refund_payment()")
    print("    - verify_payment_status()")

    print("\n✓ Each role has ONLY the methods it needs - no unused interface methods!")


def demo_dip_dependency_injection():
    """
    DIP: Dependency Inversion Principle

    High-level modules (services) depend on abstractions (interfaces),
    not concrete implementations. This allows flexible component substitution.
    """
    print("\n" + "=" * 70)
    print("DEMO 6: DIP - Dependency Inversion Principle")
    print("=" * 70)

    # Create repositories (abstraction)
    flight_repo = InMemoryRepository()
    booking_repo = InMemoryRepository()

    # Add flights to repository
    flights = create_sample_flights()
    for flight in flights:
        flight_repo.add(flight.flight_number, flight)

    # Create services with dependency injection
    print("\n✓ Services depend on abstractions, not concrete implementations:\n")

    flight_service = FlightService(flight_repo)
    print(f"  FlightService initialized with: {type(flight_repo).__name__}")

    booking_service = BookingService(
        booking_repo,
        pricing_strategy=DynamicPricing(100.0),
        seating_strategy=SequentialAllocation(["1A", "1B", "1C"]),
    )
    print(f"  BookingService initialized with:")
    print(f"    - Repository: {type(booking_repo).__name__}")
    print(f"    - Pricing: {booking_service.pricing_strategy.get_strategy_name()}")
    print(f"    - Seating: {booking_service.seating_strategy.get_strategy_name()}")

    # Payment service with different gateways
    payment_gateways = [
        StripeGateway(api_key="sk_test_123"),
        PayPalGateway(client_id="client_123"),
        CreditCardGateway(merchant_id="merchant_123"),
    ]

    print(f"\n  PaymentService can use any payment gateway:")
    for gateway in payment_gateways:
        print(f"    ✓ {gateway.get_gateway_name()}")

    # Notifiers (different channels implementing same interface)
    notifiers = [
        EmailNotifier(smtp_server="smtp.example.com"),
        SMSNotifier(api_key="sms_api_key"),
        PushNotifier(api_key="push_api_key"),
    ]

    print(f"\n  Multiple notification channels:")
    for notifier in notifiers:
        print(f"    ✓ {notifier.get_channel_name()}")

    print("\n✓ Different implementations can be swapped without changing service code!")

    # Demonstrate actual usage
    print("\n✓ Complete booking flow with DIP:")

    passengers = create_sample_passengers()
    flight = flights[0]

    # Create booking
    booking = booking_service.create_booking(
        passenger_ids=[passengers[0].passenger_id, passengers[1].passenger_id],
        flight_id=flight.flight_number,
    )
    print(f"  1. Created booking: {booking.booking_id}")

    # Set pricing strategy
    booking_service.set_pricing_strategy(LoyaltyPricing(flight.price))
    price = booking_service.calculate_booking_price(len(booking.passenger_ids))
    booking.total_price = price
    booking_repo.update(booking.booking_id, booking)
    print(f"  2. Set pricing strategy and calculated: {format_currency(price)}")

    # Process payment
    payment_service = PaymentService(StripeGateway())
    result = payment_service.process_booking_payment(
        booking,
        customer_details={"name": passengers[0].full_name, "email": passengers[0].email},
        payment_details={"card_token": "tok_123"},
    )
    print(f"  3. Processed payment: {result['status']}")

    # Confirm booking
    booking_service.confirm_booking(booking.booking_id)
    print(f"  4. Confirmed booking")


def demo_complete_booking_flow():
    """
    Complete Flight Booking Demo

    Demonstrates how all SOLID principles work together
    in a complete booking flow.
    """
    print("\n" + "=" * 70)
    print("DEMO 7: Complete Flight Booking Flow")
    print("=" * 70)

    # Initialize system
    flight_repo = InMemoryRepository()
    booking_repo = InMemoryRepository()

    # Create and add flights
    flights = create_sample_flights()
    for flight in flights:
        flight_repo.add(flight.flight_number, flight)

    # Initialize services
    flight_service = FlightService(flight_repo)
    booking_service = BookingService(
        booking_repo,
        pricing_strategy=DynamicPricing(base_price=250.0),
    )

    # Get passengers
    passengers = create_sample_passengers()

    # Search for flights
    print("\n1. SEARCH FLIGHTS")
    print(f"   Searching: {passengers[0].full_name} (Adult) and {passengers[2].full_name} (Child)")
    available_flights = flight_service.search_flights("New York", "Los Angeles", min_available_seats=2)
    print(f"   Found {len(available_flights)} flight(s)")

    if available_flights:
        selected_flight = available_flights[0]
        print(f"   Selected: {selected_flight.flight_number} at {format_currency(selected_flight.price)}")

        # Reserve seats
        print("\n2. RESERVE SEATS")
        flight_service.reserve_seats(selected_flight.flight_number, 2)
        print(f"   Reserved 2 seats")

        # Create booking
        print("\n3. CREATE BOOKING")
        booking = booking_service.create_booking(
            passenger_ids=[passengers[0].passenger_id, passengers[2].passenger_id],
            flight_id=selected_flight.flight_number,
        )
        print(f"   Booking ID: {booking.booking_id}")

        # Calculate price
        print("\n4. CALCULATE PRICE")
        occupancy = 100 - selected_flight.get_occupancy_rate()
        days_until = (selected_flight.departure_time - datetime.now()).days
        price = booking_service.calculate_booking_price(
            num_passengers=2,
            occupancy_rate=occupancy,
            days_until_departure=days_until,
            passenger_type="ADULT",
        )
        booking.total_price = price
        booking_repo.update(booking.booking_id, booking)
        print(f"   Total price: {format_currency(price)}")

        # Process payment
        print("\n5. PROCESS PAYMENT")
        payment_service = PaymentService(StripeGateway())
        payment_result = payment_service.process_booking_payment(
            booking,
            customer_details={
                "name": passengers[0].full_name,
                "email": passengers[0].email,
            },
            payment_details={"card_token": "tok_visa_123"},
        )
        print(f"   Status: {payment_result['status']}")
        print(f"   Reference: {payment_result['reference_id']}")

        # Confirm and check in
        print("\n6. CONFIRM AND CHECK-IN")
        booking_service.confirm_booking(booking.booking_id)
        booking_service.pay_booking(booking.booking_id, price)
        booking_service.check_in_booking(booking.booking_id)
        print(f"   Status: {booking.status.value}")

        # Get summary
        print("\n7. BOOKING SUMMARY")
        summary = booking.get_summary()
        for key, value in summary.items():
            print(f"   {key}: {value}")


def main():
    """Main entry point for the Flight Booking System demo."""
    print("\n")
    print("[" + "=" * 68 + "]")
    print("|" + " " * 15 + "FLIGHT BOOKING SYSTEM - SOLID PRINCIPLES DEMO" + " " * 9 + "|")
    print("[" + "=" * 68 + "]")

    try:
        # Run all demos
        demo_srp_solid_principle()
        demo_ocp_pricing_strategies()
        demo_ocp_seating_strategies()
        demo_lsp_aircraft_substitution()
        demo_isp_segregated_interfaces()
        demo_dip_dependency_injection()
        demo_complete_booking_flow()

        print("\n" + "=" * 70)
        print("✓ All SOLID principles demonstrated successfully!")
        print("=" * 70 + "\n")

    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
