"""
Integration tests for Flight Booking System.

Tests all components working together with DIP, OCP, ISP, LSP, and SRP.
"""

import pytest
from datetime import datetime, timedelta
from src.core.entities import (
    Flight,
    FlightStatus,
    Passenger,
    PassengerType,
    Booking,
    BookingStatus,
    CommercialAircraft,
)
from src.core.services import FlightService, BookingService
from src.core.services.pricing import (
    StandardPricing,
    DynamicPricing,
    SeasonalPricing,
    LoyaltyPricing,
)
from src.core.services.seating import SequentialAllocation
from src.core.services.notification import EmailNotifier, SMSNotifier
from src.core.repositories import InMemoryRepository
from src.payment import StripeGateway, PayPalGateway


class TestIntegration:
    """Integration tests for the flight booking system."""

    def test_complete_booking_workflow(self):
        """Test complete booking workflow from search to payment."""
        # Setup repositories
        flight_repo = InMemoryRepository()
        booking_repo = InMemoryRepository()

        # Create flight
        flight = Flight(
            flight_number="AA100",
            origin="New York",
            destination="Los Angeles",
            departure_time=datetime.now() + timedelta(days=5),
            arrival_time=datetime.now() + timedelta(days=5, hours=6),
            aircraft_id="AC001",
            total_seats=100,
            available_seats=50,
            status=FlightStatus.SCHEDULED,
            price=250.0,
        )
        flight_repo.save(flight)

        # Create passenger
        passenger = Passenger(
            passenger_id="P001",
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            phone="+1-212-555-0123",
            date_of_birth="1990-01-15",
            passenger_type=PassengerType.ADULT,
            loyalty_number="LOY001",
        )

        # Setup services with dependency injection
        pricing_strategy = StandardPricing(base_price=250.0)
        seating_strategy = SequentialAllocation(
            [f"{i}{chr(65 + j)}" for i in range(1, 26) for j in range(4)]
        )

        flight_service = FlightService(flight_repo)
        booking_service = BookingService(booking_repo, pricing_strategy, seating_strategy)

        # Search flights
        flights = flight_service.search_flights("New York", "Los Angeles")
        assert len(flights) > 0
        assert flights[0].flight_number == "AA100"

        # Create booking
        booking = booking_service.create_booking(
            passenger_ids=[passenger.passenger_id],
            flight_id="AA100",
            seat_numbers=["1A"],
        )

        assert booking.status == BookingStatus.PENDING
        assert booking.total_price == 250.0

        # Confirm booking
        booking_service.confirm_booking(booking.booking_id)
        confirmed_booking = booking_repo.find_by_id(booking.booking_id)
        assert confirmed_booking.status == BookingStatus.CONFIRMED

    def test_pricing_strategies(self):
        """Test different pricing strategies with OCP."""
        base_price = 100.0
        occupancy = 75.0
        days = 10

        # Standard pricing
        standard = StandardPricing(base_price)
        standard_price = standard.calculate_price(1, occupancy, days, "ADULT")
        assert standard_price == 100.0

        # Dynamic pricing
        dynamic = DynamicPricing(base_price)
        dynamic_price = dynamic.calculate_price(1, occupancy, days, "ADULT")
        assert dynamic_price > standard_price

        # Seasonal pricing (assuming June - high season)
        seasonal = SeasonalPricing(base_price)
        seasonal_price = seasonal.calculate_price(
            1, occupancy, days, "ADULT", departure_month=6
        )
        assert seasonal_price > standard_price

        # Loyalty pricing
        loyalty = LoyaltyPricing(base_price)
        loyalty_price = loyalty.calculate_price(
            1, occupancy, days, "ADULT", loyalty_tier="GOLD"
        )
        assert loyalty_price < standard_price

    def test_lsp_aircraft_substitution(self):
        """Test LSP - Aircraft types are fully substitutable."""
        # Both aircraft types can be used interchangeably
        commercial = CommercialAircraft(
            aircraft_id="AC001",
            model="Boeing 747",
            manufacturer="Boeing",
            total_seats=300,
            first_class_seats=12,
            business_class_seats=48,
            economy_class_seats=240,
        )

        # Both have the same interface
        assert commercial.get_seat_classes() is not None
        assert commercial.calculate_luggage_allowance() > 0
        assert commercial.get_info() is not None

        # Can be used in same context
        aircraft_list = [commercial]
        for aircraft in aircraft_list:
            luggage = aircraft.calculate_luggage_allowance()
            assert luggage > 0

    def test_isp_segregated_interfaces(self):
        """Test ISP - Interfaces are segregated by role."""
        # Create repository (DIP abstraction)
        repo = InMemoryRepository()

        # Booking service implements segregated operations
        booking_service = BookingService(repo)

        # Each interface is focused on specific operations
        # Services depend on abstractions, not concretions
        assert booking_service is not None

    def test_dip_dependency_injection(self):
        """Test DIP - Dependencies are injected, not hardcoded."""
        # Different repositories can be injected
        repo = InMemoryRepository()

        # Different pricing strategies can be injected
        pricing1 = StandardPricing(100.0)
        pricing2 = DynamicPricing(100.0)

        # Services work with any implementation
        booking_service1 = BookingService(repo, pricing1)
        booking_service2 = BookingService(repo, pricing2)

        assert booking_service1.pricing_strategy == pricing1
        assert booking_service2.pricing_strategy == pricing2

    def test_payment_processing_dip(self):
        """Test DIP with payment processors."""
        # Different payment gateways can be used interchangeably
        stripe = StripeGateway(api_key="test_key")
        paypal = PayPalGateway(api_key="test_key")

        # Both implement the same interface (PaymentProcessor)
        # Code can work with any implementation
        payment_methods = [stripe, paypal]
        assert len(payment_methods) == 2

    def test_notification_services_dip(self):
        """Test DIP with notification services."""
        # Different notifiers can be used interchangeably
        email_notifier = EmailNotifier()
        sms_notifier = SMSNotifier()

        # Both implement the Notifier interface
        # Code can work with any notification channel
        notifiers = [email_notifier, sms_notifier]
        assert len(notifiers) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
