"""
DIP (Dependency Inversion Principle) Demo

DIP states that high-level modules should not depend on low-level modules.
Both should depend on abstractions.

In this demo:
- Services depend on interfaces, not concrete implementations
- Payment gateways can be swapped
- Notifiers can be swapped
- Repositories can be swapped
"""


def demo_dip():
    """Demonstrate Dependency Inversion Principle."""
    from src.core.repositories import InMemoryRepository
    from src.core.services import FlightService, BookingService, PaymentService
    from src.core.services.pricing import DynamicPricing, LoyaltyPricing
    from src.core.services.seating import SequentialAllocation, WindowPriority
    from src.core.services.notification import EmailNotifier, SMSNotifier, PushNotifier
    from src.payment import StripeGateway, PayPalGateway, CreditCardGateway
    from src.core.entities import Flight, FlightStatus, Passenger, PassengerType
    from datetime import datetime, timedelta
    from src.utils import format_currency

    print("\n" + "=" * 70)
    print("DIP: Dependency Inversion Principle Demo")
    print("=" * 70)

    print("\n[OK] Services depend on abstractions, not concrete implementations:\n")

    # Create repositories (abstractions)
    flight_repo = InMemoryRepository()
    booking_repo = InMemoryRepository()

    # Create services with injected dependencies
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

    # Payment gateways are interchangeable
    payment_gateways = [
        StripeGateway(api_key="sk_test_123"),
        PayPalGateway(client_id="client_123"),
        CreditCardGateway(merchant_id="merchant_123"),
    ]

    print(f"\n  PaymentService can use any payment gateway:")
    for gateway in payment_gateways:
        print(f"    [OK] {gateway.get_gateway_name()}")

    # Notifiers are interchangeable
    notifiers = [
        EmailNotifier(smtp_server="smtp.example.com"),
        SMSNotifier(api_key="sms_api_key"),
        PushNotifier(api_key="push_api_key"),
    ]

    print(f"\n  Multiple notification channels:")
    for notifier in notifiers:
        print(f"    [OK] {notifier.get_channel_name()}")

    print("\n[OK] Different implementations can be swapped without changing service code!")

    # Demonstrate complete booking flow
    print("\n[OK] Complete booking flow with DIP:")

    # Create sample data
    flight = Flight(
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

    passenger2 = Passenger(
        passenger_id="P002",
        first_name="Tommy",
        last_name="Smith",
        email="tommy.smith@example.com",
        phone="+1-212-555-0125",
        date_of_birth="2010-08-10",
        passenger_type=PassengerType.CHILD,
    )

    # Add flight to repository
    flight_repo.add(flight.flight_number, flight)

    # Create booking
    booking = booking_service.create_booking(
        passenger_ids=[passenger1.passenger_id, passenger2.passenger_id],
        flight_id=flight.flight_number,
    )
    print(f"  1. Created booking: {booking.booking_id}")

    # Calculate price with injected strategy
    booking_service.set_pricing_strategy(LoyaltyPricing(flight.price))
    price = booking_service.calculate_booking_price(2)
    booking.total_price = price
    booking_repo.update(booking.booking_id, booking)
    print(f"  2. Set pricing strategy and calculated: {format_currency(price)}")

    # Process payment with injected gateway
    payment_service = PaymentService(StripeGateway(api_key="sk_test_123"))
    result = payment_service.process_booking_payment(
        booking,
        customer_details={"name": passenger1.full_name, "email": passenger1.email},
        payment_details={"card_token": "tok_123"},
    )
    print(f"  3. Processed payment: {result['status']}")

    # Confirm booking
    booking_service.confirm_booking(booking.booking_id)
    print(f"  4. Confirmed booking")

    print("\n[OK] DIP Demonstrated: All dependencies are injected, not hardcoded!")


if __name__ == "__main__":
    demo_dip() 
