import json
import os
from datetime import datetime
from typing import List, Dict, Optional
import re

# ===================== FLIGHT DATA =====================

class Flight:
    def __init__(self, flight_id: str, airline: str, departure: str, arrival: str,
                 departure_time: str, arrival_time: str, duration: str, price: float,
                 seats_available: int):
        self.flight_id = flight_id
        self.airline = airline
        self.departure = departure
        self.arrival = arrival
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.duration = duration
        self.price = price
        self.seats_available = seats_available

    def to_dict(self):
        return {
            'flight_id': self.flight_id,
            'airline': self.airline,
            'departure': self.departure,
            'arrival': self.arrival,
            'departure_time': self.departure_time,
            'arrival_time': self.arrival_time,
            'duration': self.duration,
            'price': self.price,
            'seats_available': self.seats_available
        }

    def display(self):
        print(f"✈️  Flight ID: {self.flight_id}")
        print(f"   Airline: {self.airline}")
        print(f"   Route: {self.departure} → {self.arrival}")
        print(f"   Departure: {self.departure_time} | Arrival: {self.arrival_time}")
        print(f"   Duration: {self.duration}")
        print(f"   Price: ${self.price:.2f}")
        print(f"   Seats Available: {self.seats_available}")
        print("-" * 60)


class Booking:
    def __init__(self, booking_id: str, passenger_name: str, email: str,
                 phone: str, flight: Flight, num_passengers: int, total_price: float):
        self.booking_id = booking_id
        self.passenger_name = passenger_name
        self.email = email
        self.phone = phone
        self.flight = flight
        self.num_passengers = num_passengers
        self.total_price = total_price
        self.booking_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status = "Confirmed"

    def to_dict(self):
        return {
            'booking_id': self.booking_id,
            'passenger_name': self.passenger_name,
            'email': self.email,
            'phone': self.phone,
            'flight': self.flight.to_dict(),
            'num_passengers': self.num_passengers,
            'total_price': self.total_price,
            'booking_date': self.booking_date,
            'status': self.status
        }

    def display(self):
        print("\n" + "=" * 60)
        print("🎟️  BOOKING CONFIRMATION")
        print("=" * 60)
        print(f"Booking ID: {self.booking_id}")
        print(f"Passenger Name: {self.passenger_name}")
        print(f"Email: {self.email}")
        print(f"Phone: {self.phone}")
        print(f"Booking Date: {self.booking_date}")
        print(f"Status: {self.status}")
        print("-" * 60)
        print("FLIGHT DETAILS:")
        print(f"  Flight: {self.flight.flight_id} ({self.flight.airline})")
        print(f"  Route: {self.flight.departure} → {self.flight.arrival}")
        print(f"  Departure: {self.flight.departure_time}")
        print(f"  Arrival: {self.flight.arrival_time}")
        print(f"  Duration: {self.flight.duration}")
        print("-" * 60)
        print(f"Number of Passengers: {self.num_passengers}")
        print(f"Price per Ticket: ${self.flight.price:.2f}")
        print(f"TOTAL PRICE: ${self.total_price:.2f}")
        print("=" * 60 + "\n")


class FlightBookingSystem:
    def __init__(self):
        self.flights = self._initialize_flights()
        self.bookings: List[Booking] = []
        self.bookings_file = "bookings.json"
        self.load_bookings()

    def _initialize_flights(self) -> List[Flight]:
        """Initialize sample flight data"""
        return [
            Flight("FL001", "SkyWings", "NYC", "LAX", "08:00 AM", "11:30 AM", "5h 30m", 299.99, 50),
            Flight("FL002", "SkyWings", "NYC", "LAX", "02:00 PM", "05:30 PM", "5h 30m", 349.99, 30),
            Flight("FL003", "AirTravels", "NYC", "LAX", "06:00 PM", "09:30 PM", "5h 30m", 279.99, 45),
            Flight("FL004", "FastAir", "NYC", "MIA", "07:00 AM", "10:30 AM", "3h 30m", 199.99, 60),
            Flight("FL005", "FastAir", "NYC", "MIA", "03:00 PM", "06:30 PM", "3h 30m", 229.99, 40),
            Flight("FL006", "SkyWings", "LAX", "CHI", "09:00 AM", "04:00 PM", "4h", 279.99, 35),
            Flight("FL007", "AirTravels", "LAX", "CHI", "01:00 PM", "08:00 PM", "4h", 319.99, 25),
            Flight("FL008", "FastAir", "LAX", "DEN", "10:00 AM", "12:30 PM", "2h 30m", 159.99, 55),
            Flight("FL009", "SkyWings", "MIA", "BOS", "06:00 AM", "09:30 AM", "3h 30m", 249.99, 38),
            Flight("FL010", "AirTravels", "MIA", "BOS", "11:00 AM", "02:30 PM", "3h 30m", 269.99, 42),
        ]

    def search_flights(self, departure: str, arrival: str) -> List[Flight]:
        """Search flights by departure and arrival airports"""
        return [f for f in self.flights 
                if f.departure.upper() == departure.upper() and f.arrival.upper() == arrival.upper()]

    def display_search_results(self, flights: List[Flight]):
        """Display search results in a formatted way"""
        if not flights:
            print("\n❌ No flights found for this route.\n")
            return

        print(f"\n✅ Found {len(flights)} flight(s) for your route:\n")
        for idx, flight in enumerate(flights, 1):
            print(f"{idx}. ", end="")
            flight.display()

    def validate_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def validate_phone(self, phone: str) -> bool:
        """Validate phone number format"""
        pattern = r'^[0-9\-\+\(\)\s]{10,}$'
        return re.match(pattern, phone) is not None

    def get_passenger_details(self) -> Dict:
        """Get passenger details from user input"""
        print("\n" + "=" * 60)
        print("📋 PASSENGER INFORMATION")
        print("=" * 60)

        while True:
            name = input("Enter passenger name: ").strip()
            if len(name) >= 2:
                break
            print("❌ Please enter a valid name (at least 2 characters).")

        while True:
            email = input("Enter email address: ").strip()
            if self.validate_email(email):
                break
            print("❌ Please enter a valid email address.")

        while True:
            phone = input("Enter phone number: ").strip()
            if self.validate_phone(phone):
                break
            print("❌ Please enter a valid phone number.")

        return {'name': name, 'email': email, 'phone': phone}

    def process_payment(self, total_price: float) -> bool:
        """Process payment with various payment methods"""
        print("\n" + "=" * 60)
        print("💳 PAYMENT PROCESSING")
        print("=" * 60)
        print(f"Total Amount Due: ${total_price:.2f}\n")

        print("Select Payment Method:")
        print("1. Credit Card")
        print("2. Debit Card")
        print("3. PayPal")
        print("4. Bank Transfer")

        while True:
            choice = input("\nEnter your choice (1-4): ").strip()
            if choice in ['1', '2', '3', '4']:
                break
            print("❌ Invalid choice. Please enter 1-4.")

        payment_methods = {
            '1': 'Credit Card',
            '2': 'Debit Card',
            '3': 'PayPal',
            '4': 'Bank Transfer'
        }

        method = payment_methods[choice]
        print(f"\n🔄 Processing payment via {method}...")

        if choice == '1' or choice == '2':
            while True:
                card_number = input("Enter card number (16 digits): ").strip().replace(" ", "")
                if len(card_number) == 16 and card_number.isdigit():
                    break
                print("❌ Please enter a valid 16-digit card number.")

            while True:
                expiry = input("Enter expiry date (MM/YY): ").strip()
                if len(expiry) == 5 and expiry[2] == '/':
                    break
                print("❌ Please enter a valid expiry date (MM/YY).")

            while True:
                cvv = input("Enter CVV (3 digits): ").strip()
                if len(cvv) == 3 and cvv.isdigit():
                    break
                print("❌ Please enter a valid 3-digit CVV.")

        elif choice == '3':
            paypal_email = input("Enter PayPal email: ").strip()
            if not self.validate_email(paypal_email):
                print("❌ Invalid PayPal email.")
                return False

        print("\n✅ Payment processed successfully!")
        return True

    def generate_booking_id(self) -> str:
        """Generate a unique booking ID"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        booking_number = f"BK{timestamp}{len(self.bookings) + 1:03d}"
        return booking_number

    def book_flight(self, flight: Flight, passenger_details: Dict, num_passengers: int) -> Optional[Booking]:
        """Complete flight booking with payment"""
        if flight.seats_available < num_passengers:
            print(f"\n❌ Not enough seats available. Only {flight.seats_available} seats left.")
            return None

        total_price = flight.price * num_passengers

        # Process payment
        if not self.process_payment(total_price):
            print("\n❌ Payment failed. Booking cancelled.")
            return None

        # Create booking
        booking_id = self.generate_booking_id()
        booking = Booking(
            booking_id=booking_id,
            passenger_name=passenger_details['name'],
            email=passenger_details['email'],
            phone=passenger_details['phone'],
            flight=flight,
            num_passengers=num_passengers,
            total_price=total_price
        )

        # Update flight availability
        flight.seats_available -= num_passengers

        # Save booking
        self.bookings.append(booking)
        self.save_bookings()

        return booking

    def save_bookings(self):
        """Save bookings to JSON file"""
        bookings_data = [booking.to_dict() for booking in self.bookings]
        with open(self.bookings_file, 'w') as f:
            json.dump(bookings_data, f, indent=4)

    def load_bookings(self):
        """Load bookings from JSON file"""
        if os.path.exists(self.bookings_file):
            try:
                with open(self.bookings_file, 'r') as f:
                    bookings_data = json.load(f)
                    # Reconstruct bookings (simplified for demo)
                    # In production, you'd want more robust deserialization
            except (json.JSONDecodeError, IOError):
                pass

    def view_booking_history(self):
        """Display all bookings for the user"""
        if not self.bookings:
            print("\n❌ No bookings found.\n")
            return

        print("\n" + "=" * 60)
        print("📚 BOOKING HISTORY")
        print("=" * 60)
        for idx, booking in enumerate(self.bookings, 1):
            print(f"\n{idx}. Booking ID: {booking.booking_id}")
            print(f"   Passenger: {booking.passenger_name}")
            print(f"   Flight: {booking.flight.flight_id} ({booking.flight.airline})")
            print(f"   Route: {booking.flight.departure} → {booking.flight.arrival}")
            print(f"   Date: {booking.booking_date}")
            print(f"   Total: ${booking.total_price:.2f}")
            print(f"   Status: {booking.status}")
            print("-" * 60)

    def display_menu(self):
        """Display main menu"""
        print("\n" + "=" * 60)
        print("🌍 INTERACTIVE FLIGHT BOOKING SYSTEM")
        print("=" * 60)
        print("1. Search Flights")
        print("2. View Booking History")
        print("3. View All Available Flights")
        print("4. Exit")
        print("=" * 60)

    def view_all_flights(self):
        """Display all available flights"""
        print("\n" + "=" * 60)
        print("✈️  ALL AVAILABLE FLIGHTS")
        print("=" * 60 + "\n")
        for flight in self.flights:
            flight.display()

    def run_search_and_book(self):
        """Handle search and booking flow"""
        print("\n" + "=" * 60)
        print("🔍 FLIGHT SEARCH")
        print("=" * 60)

        print("\nAvailable airports: NYC, LAX, MIA, CHI, BOS, DEN\n")

        while True:
            departure = input("Enter departure airport code: ").strip().upper()
            if len(departure) == 3 and departure.isalpha():
                break
            print("❌ Please enter a valid 3-letter airport code.")

        while True:
            arrival = input("Enter arrival airport code: ").strip().upper()
            if len(arrival) == 3 and arrival.isalpha():
                break
            print("❌ Please enter a valid 3-letter airport code.")

        if departure == arrival:
            print("\n❌ Departure and arrival airports cannot be the same.")
            return

        # Search flights
        flights = self.search_flights(departure, arrival)
        self.display_search_results(flights)

        if not flights:
            return

        # Select flight
        while True:
            try:
                selection = int(input("Select flight number to book (or 0 to cancel): ").strip())
                if selection == 0:
                    return
                if 1 <= selection <= len(flights):
                    selected_flight = flights[selection - 1]
                    break
                print("❌ Invalid selection. Please try again.")
            except ValueError:
                print("❌ Please enter a valid number.")

        # Get number of passengers
        while True:
            try:
                num_passengers = int(input("How many passengers? ").strip())
                if 1 <= num_passengers <= selected_flight.seats_available:
                    break
                print(f"❌ Please enter a number between 1 and {selected_flight.seats_available}.")
            except ValueError:
                print("❌ Please enter a valid number.")

        # Get passenger details
        passenger_details = self.get_passenger_details()

        # Confirm booking
        total_price = selected_flight.price * num_passengers
        print("\n" + "=" * 60)
        print("📋 BOOKING SUMMARY")
        print("=" * 60)
        print(f"Flight: {selected_flight.flight_id} ({selected_flight.airline})")
        print(f"Route: {selected_flight.departure} → {selected_flight.arrival}")
        print(f"Departure: {selected_flight.departure_time}")
        print(f"Passengers: {num_passengers}")
        print(f"Price per ticket: ${selected_flight.price:.2f}")
        print(f"Total: ${total_price:.2f}")

        confirm = input("\nProceed with booking? (yes/no): ").strip().lower()
        if confirm != 'yes':
            print("\n❌ Booking cancelled.")
            return

        # Book flight
        booking = self.book_flight(selected_flight, passenger_details, num_passengers)
        if booking:
            booking.display()
            print("✅ A confirmation email has been sent to your email address.")
            print(f"📧 Check your inbox for: {passenger_details['email']}")

    def run(self):
        """Main application loop"""
        print("\n" + "=" * 60)
        print("🎉 WELCOME TO FLIGHT BOOKING SYSTEM 🎉")
        print("=" * 60)

        while True:
            self.display_menu()
            choice = input("Enter your choice (1-4): ").strip()

            if choice == '1':
                self.run_search_and_book()
            elif choice == '2':
                self.view_booking_history()
            elif choice == '3':
                self.view_all_flights()
            elif choice == '4':
                print("\n" + "=" * 60)
                print("👋 Thank you for using Flight Booking System!")
                print("Have a great flight! ✈️")
                print("=" * 60 + "\n")
                break
            else:
                print("❌ Invalid choice. Please enter 1-4.")


# ===================== MAIN ENTRY POINT =====================

if __name__ == "__main__":
    system = FlightBookingSystem()
    system.run()
