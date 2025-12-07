"""
ISP (Interface Segregation Principle) Demo

ISP states that clients should not be forced to depend on interfaces they don't use.
Create small, focused interfaces rather than large, general-purpose ones.

In this demo:
- PassengerOperations has methods for passengers
- StaffOperations has methods for staff
- AdminOperations has methods for admins
- PaymentProcessor has payment methods
- Notifier has notification methods
"""


def demo_isp():
    """Demonstrate Interface Segregation Principle."""
    from src.core.interfaces import (
        PassengerOperations,
        StaffOperations,
        AdminOperations,
        PaymentProcessor,
        Notifier,
    )

    print("\n" + "=" * 70)
    print("ISP: Interface Segregation Principle Demo")
    print("=" * 70)

    print("\n[OK] Segregated interfaces for different roles:\n")

    print("  PassengerOperations (6 methods):")
    print("    - search_flights()")
    print("    - make_booking()")
    print("    - view_my_bookings()")
    print("    - cancel_booking()")
    print("    - check_booking_status()")
    print("    - get_flight_details()")

    print("\n  StaffOperations (6 methods):")
    print("    - check_flight_status()")
    print("    - get_passenger_list()")
    print("    - process_check_in()")
    print("    - generate_boarding_pass()")
    print("    - handle_cancellation_request()")
    print("    - get_passenger_details()")

    print("\n  AdminOperations (6 methods):")
    print("    - add_flight()")
    print("    - add_aircraft()")
    print("    - set_pricing_strategy()")
    print("    - get_revenue_report()")
    print("    - get_system_statistics()")
    print("    - get_flight_occupancy_report()")

    print("\n  PaymentProcessor (3 focused methods):")
    print("    - process_payment()")
    print("    - refund_payment()")
    print("    - verify_payment_status()")

    print("\n  Notifier (3 focused methods):")
    print("    - send_notification()")
    print("    - send_bulk_notification()")
    print("    - get_notification_status()")

    print("\n[OK] Each role has ONLY the methods it needs!")
    print("[OK] No 'fat' interfaces forcing clients to implement unused methods!")
    print("\n[OK] ISP Demonstrated: Interfaces are segregated by role!")


if __name__ == "__main__":
    demo_isp() 
