"""
SRP (Single Responsibility Principle) Demo

SRP states that a class should have only one reason to change.
Each class should have a single, well-defined responsibility.

In this demo:
- Flight class: Only responsible for flight data and seat management
- Passenger class: Only responsible for passenger profile
- Booking class: Only responsible for booking lifecycle
"""


def demo_srp():
    """Demonstrate Single Responsibility Principle."""
    from datetime import datetime, timedelta
    from src.core.entities import Flight, FlightStatus, Passenger, PassengerType, Booking, BookingStatus

    print("\n" + "=" * 70)
    print("SRP: Single Responsibility Principle Demo")
    print("=" * 70)

    # SRP: Flight class - ONLY manages flight data and seats
    print("\n1. Flight Entity (Responsibility: Flight data & seat management)")
    print("-" * 70)

    flight = Flight(
        flight_number="AA100",
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

    print(f"Flight: {flight.flight_number}")
    print(f"Route: {flight.origin} → {flight.destination}")
    print(f"Total seats: {flight.total_seats}")
    print(f"Available: {flight.available_seats}")
    print(f"Occupancy: {flight.get_occupancy_rate():.1f}%")

    # Reserve seats
    print("\nReserving 10 seats...")
    if flight.reserve_seat(10):
        print(f"✓ Reserved successfully. Available now: {flight.available_seats}")

    # SRP: Passenger class - ONLY manages passenger profile
    print("\n2. Passenger Entity (Responsibility: Passenger profile)")
    print("-" * 70)

    passenger = Passenger(
        passenger_id="P001",
        first_name="John",
        last_name="Smith",
        email="john.smith@example.com",
        phone="+1-212-555-0123",
        date_of_birth="1990-01-15",
        passenger_type=PassengerType.ADULT,
        loyalty_number="LOY001",
    )

    print(f"Passenger: {passenger.full_name}")
    print(f"Email: {passenger.email}")
    print(f"Phone: {passenger.phone}")
    print(f"Type: {passenger.passenger_type.value}")
    print(f"Loyalty #: {passenger.loyalty_number}")
    print(f"Profile: {passenger.get_profile()}")

    # SRP: Booking class - ONLY manages booking lifecycle
    print("\n3. Booking Entity (Responsibility: Booking lifecycle)")
    print("-" * 70)

    booking = Booking(
        booking_id="BK001",
        flight_id=flight.flight_number,
        passenger_ids=[passenger.passenger_id],
        seat_numbers=["10A"],
        booking_date=datetime.now(),
        status=BookingStatus.PENDING,
        total_price=250.0,
    )

    print(f"Booking ID: {booking.booking_id}")
    print(f"Flight: {booking.flight_id}")
    print(f"Passengers: {len(booking.passenger_ids)}")
    print(f"Seats: {booking.seat_numbers}")
    print(f"Status: {booking.status.value}")
    print(f"Total Price: ${booking.total_price:.2f}")

    # Process booking lifecycle
    print("\nProcessing booking workflow:")
    booking.mark_as_confirmed()
    print(f"✓ Confirmed - Status: {booking.status.value}")

    booking.record_payment(250.0)
    print(f"✓ Payment recorded - Status: {booking.status.value}")

    booking.mark_as_paid()
    print(f"✓ Paid - Status: {booking.status.value}")

    booking.mark_as_checked_in()
    print(f"✓ Checked in - Status: {booking.status.value}")

    print("\n✓ SRP Demonstrated: Each entity has ONE clear responsibility!")


if __name__ == "__main__":
    demo_srp()
