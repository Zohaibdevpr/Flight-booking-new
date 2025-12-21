import json
import os
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import hashlib
import random
import string

# ==================== DATA PERSISTENCE ====================

class DataManager:
    """Manages persistent data storage using JSON files"""
    
    FLIGHTS_FILE = "flights_data.json"
    BOOKINGS_FILE = "bookings_data.json"
    
    @staticmethod
    def load_flights() -> List[Dict]:
        """Load flights from JSON file"""
        if os.path.exists(DataManager.FLIGHTS_FILE):
            try:
                with open(DataManager.FLIGHTS_FILE, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return DataManager.get_default_flights()
        return DataManager.get_default_flights()
    
    @staticmethod
    def get_default_flights() -> List[Dict]:
        """Return default flights data"""
        return [
            {
                "flight_id": "FL001",
                "airline": "SkyWings Airlines",
                "departure_city": "New York",
                "arrival_city": "Los Angeles",
                "departure_time": "2025-12-25 08:00",
                "arrival_time": "2025-12-25 11:30",
                "duration": "5h 30m",
                "price": 250.00,
                "available_seats": 50,
                "total_seats": 100
            },
            {
                "flight_id": "FL002",
                "airline": "AeroConnect",
                "departure_city": "New York",
                "arrival_city": "Chicago",
                "departure_time": "2025-12-25 10:00",
                "arrival_time": "2025-12-25 13:00",
                "duration": "3h",
                "price": 180.00,
                "available_seats": 30,
                "total_seats": 100
            },
            {
                "flight_id": "FL003",
                "airline": "SkyWings Airlines",
                "departure_city": "Los Angeles",
                "arrival_city": "Miami",
                "departure_time": "2025-12-26 14:00",
                "arrival_time": "2025-12-26 20:00",
                "duration": "4h 30m",
                "price": 220.00,
                "available_seats": 45,
                "total_seats": 100
            },
            {
                "flight_id": "FL004",
                "airline": "CloudJet",
                "departure_city": "Chicago",
                "arrival_city": "Miami",
                "departure_time": "2025-12-25 16:00",
                "arrival_time": "2025-12-25 22:00",
                "duration": "5h",
                "price": 200.00,
                "available_seats": 25,
                "total_seats": 100
            },
            {
                "flight_id": "FL005",
                "airline": "AeroConnect",
                "departure_city": "Los Angeles",
                "arrival_city": "New York",
                "departure_time": "2025-12-27 09:00",
                "arrival_time": "2025-12-27 17:00",
                "duration": "5h 30m",
                "price": 260.00,
                "available_seats": 60,
                "total_seats": 100
            }
        ]
    
    @staticmethod
    def save_flights(flights: List[Dict]) -> bool:
        """Save flights to JSON file"""
        try:
            with open(DataManager.FLIGHTS_FILE, 'w') as f:
                json.dump(flights, f, indent=2)
            return True
        except IOError as e:
            print(f"Error saving flights: {e}")
            return False
    
    @staticmethod
    def load_bookings() -> List[Dict]:
        """Load bookings from JSON file"""
        if os.path.exists(DataManager.BOOKINGS_FILE):
            try:
                with open(DataManager.BOOKINGS_FILE, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []
    
    @staticmethod
    def save_bookings(bookings: List[Dict]) -> bool:
        """Save bookings to JSON file"""
        try:
            with open(DataManager.BOOKINGS_FILE, 'w') as f:
                json.dump(bookings, f, indent=2)
            return True
        except IOError as e:
            print(f"Error saving bookings: {e}")
            return False


# ==================== INPUT VALIDATION ====================

class Validator:
    """Handles all input validation"""
    
    @staticmethod
    def validate_name(name: str) -> Tuple[bool, str]:
        """Validate passenger name"""
        name = name.strip()
        if not name:
            return False, "Name cannot be empty"
        if len(name) < 2:
            return False, "Name must be at least 2 characters long"
        if len(name) > 50:
            return False, "Name must not exceed 50 characters"
        if not re.match(r"^[a-zA-Z\s'-]+$", name):
            return False, "Name can only contain letters, spaces, hyphens, and apostrophes"
        return True, "Valid"
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        """Validate email address"""
        email = email.strip().lower()
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            return False, "Invalid email format"
        if len(email) > 100:
            return False, "Email is too long"
        return True, "Valid"
    
    @staticmethod
    def validate_phone(phone: str) -> Tuple[bool, str]:
        """Validate phone number"""
        phone = phone.strip()
        # Remove common separators
        phone_cleaned = re.sub(r'[\s\-\(\)\.+]', '', phone)
        if not phone_cleaned.isdigit():
            return False, "Phone must contain only digits and optional separators"
        if len(phone_cleaned) < 7:
            return False, "Phone number is too short"
        if len(phone_cleaned) > 15:
            return False, "Phone number is too long"
        return True, "Valid"
    
    @staticmethod
    def validate_passport(passport: str) -> Tuple[bool, str]:
        """Validate passport number"""
        passport = passport.strip().upper()
        if not passport:
            return False, "Passport number cannot be empty"
        if len(passport) < 5:
            return False, "Passport number is too short"
        if len(passport) > 20:
            return False, "Passport number is too long"
        if not re.match(r'^[A-Z0-9]+$', passport):
            return False, "Passport can only contain letters and numbers"
        return True, "Valid"
    
    @staticmethod
    def validate_date(date_str: str, date_format: str = "%Y-%m-%d") -> Tuple[bool, str]:
        """Validate date format and value"""
        try:
            date_obj = datetime.strptime(date_str, date_format)
            return True, "Valid"
        except ValueError:
            return False, f"Invalid date format. Expected {date_format}"
    
    @staticmethod
    def validate_dob(dob_str: str) -> Tuple[bool, str]:
        """Validate date of birth"""
        is_valid, msg = Validator.validate_date(dob_str, "%Y-%m-%d")
        if not is_valid:
            return False, msg
        
        try:
            dob = datetime.strptime(dob_str, "%Y-%m-%d")
            age = (datetime.now() - dob).days // 365
            if age < 0:
                return False, "Date of birth cannot be in the future"
            if age < 1:
                return False, "Passenger must be at least 1 year old"
            if age > 150:
                return False, "Invalid age"
            return True, "Valid"
        except ValueError:
            return False, "Invalid date of birth"
    
    @staticmethod
    def validate_card_number(card_number: str) -> Tuple[bool, str]:
        """Validate credit card number using Luhn algorithm"""
        card_number = card_number.strip().replace(" ", "").replace("-", "")
        
        if not card_number.isdigit():
            return False, "Card number must contain only digits"
        
        if len(card_number) < 13 or len(card_number) > 19:
            return False, "Card number must be between 13 and 19 digits"
        
        # Luhn algorithm
        total = 0
        reverse_digits = card_number[::-1]
        for i, digit in enumerate(reverse_digits):
            d = int(digit)
            if i % 2 == 1:
                d *= 2
                if d > 9:
                    d -= 9
            total += d
        
        if total % 10 != 0:
            return False, "Invalid card number"
        
        return True, "Valid"
    
    @staticmethod
    def validate_expiry(expiry_str: str) -> Tuple[bool, str]:
        """Validate card expiry date (MM/YY format)"""
        expiry = expiry_str.strip()
        if not re.match(r'^\d{2}/\d{2}$', expiry):
            return False, "Expiry must be in MM/YY format"
        
        try:
            month, year = expiry.split('/')
            month = int(month)
            year = int(year)
            
            if month < 1 or month > 12:
                return False, "Invalid month"
            
            # Assuming 2000s
            expiry_date = datetime(2000 + year, month, 1)
            if expiry_date < datetime.now():
                return False, "Card is expired"
            
            return True, "Valid"
        except (ValueError, IndexError):
            return False, "Invalid expiry format"
    
    @staticmethod
    def validate_cvv(cvv: str) -> Tuple[bool, str]:
        """Validate CVV"""
        cvv = cvv.strip()
        if not cvv.isdigit():
            return False, "CVV must contain only digits"
        if len(cvv) not in [3, 4]:
            return False, "CVV must be 3 or 4 digits"
        return True, "Valid"


# ==================== FLIGHT SEARCH ====================

class FlightSearch:
    """Handles flight searching and filtering"""
    
    def __init__(self, flights: List[Dict]):
        self.flights = flights
    
    def search(self, departure: str, arrival: str, date: str) -> List[Dict]:
        """
        Search for flights based on criteria
        Args:
            departure: Departure city
            arrival: Arrival city
            date: Travel date (YYYY-MM-DD)
        """
        departure = departure.strip().lower()
        arrival = arrival.strip().lower()
        
        results = []
        for flight in self.flights:
            if (flight['departure_city'].lower() == departure and
                flight['arrival_city'].lower() == arrival and
                flight['departure_time'].startswith(date) and
                flight['available_seats'] > 0):
                results.append(flight)
        
        return results
    
    def get_all_cities(self) -> set:
        """Get all available cities"""
        cities = set()
        for flight in self.flights:
            cities.add(flight['departure_city'])
            cities.add(flight['arrival_city'])
        return sorted(list(cities))


# ==================== PASSENGER DETAILS ====================

class PassengerDetails:
    """Manages passenger information"""
    
    def __init__(self):
        self.passengers: List[Dict] = []
    
    def add_passenger(self, name: str, email: str, phone: str, 
                     dob: str, passport: str, seat_number: Optional[str] = None) -> bool:
        """Add a new passenger with validation"""
        # Validate all inputs
        validations = [
            (Validator.validate_name(name), "Name"),
            (Validator.validate_email(email), "Email"),
            (Validator.validate_phone(phone), "Phone"),
            (Validator.validate_dob(dob), "Date of Birth"),
            (Validator.validate_passport(passport), "Passport")
        ]
        
        for (is_valid, msg), field in validations:
            if not is_valid:
                print(f"❌ {field} validation failed: {msg}")
                return False
        
        # Auto-assign seat if not provided
        if not seat_number:
            seat_number = f"A{len(self.passengers) + 1}"
        
        passenger = {
            "name": name.strip(),
            "email": email.strip().lower(),
            "phone": phone.strip(),
            "dob": dob,
            "passport": passport.strip().upper(),
            "seat_number": seat_number
        }
        
        self.passengers.append(passenger)
        return True
    
    def get_passengers(self) -> List[Dict]:
        """Get all added passengers"""
        return self.passengers
    
    def clear(self):
        """Clear all passengers"""
        self.passengers = []


# ==================== PAYMENT PROCESSING ====================

class PaymentProcessor:
    """Handles payment processing and validation"""
    
    @staticmethod
    def validate_payment_info(cardholder: str, card_number: str, 
                             expiry: str, cvv: str) -> Tuple[bool, str]:
        """Validate all payment information"""
        # Validate cardholder name
        is_valid, msg = Validator.validate_name(cardholder)
        if not is_valid:
            return False, f"Cardholder name: {msg}"
        
        # Validate card number
        is_valid, msg = Validator.validate_card_number(card_number)
        if not is_valid:
            return False, f"Card number: {msg}"
        
        # Validate expiry
        is_valid, msg = Validator.validate_expiry(expiry)
        if not is_valid:
            return False, f"Expiry: {msg}"
        
        # Validate CVV
        is_valid, msg = Validator.validate_cvv(cvv)
        if not is_valid:
            return False, f"CVV: {msg}"
        
        return True, "Payment information is valid"
    
    @staticmethod
    def process_payment(amount: float, cardholder: str, card_number: str,
                       expiry: str, cvv: str) -> Tuple[bool, str, str]:
        """
        Process payment
        Returns: (success, message, transaction_id)
        """
        # Validate payment info
        is_valid, msg = PaymentProcessor.validate_payment_info(
            cardholder, card_number, expiry, cvv
        )
        if not is_valid:
            return False, msg, ""
        
        # Simulate payment processing
        if amount <= 0:
            return False, "Amount must be greater than 0", ""
        
        if amount > 10000:
            return False, "Amount exceeds maximum limit", ""
        
        # Generate transaction ID
        transaction_id = PaymentProcessor._generate_transaction_id()
        
        # Simulate random payment failure (10% chance)
        if random.random() < 0.1:
            return False, "Payment declined by bank. Please try again.", ""
        
        return True, f"Payment of ${amount:.2f} processed successfully", transaction_id
    
    @staticmethod
    def _generate_transaction_id() -> str:
        """Generate a unique transaction ID"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        return f"TXN-{timestamp}-{random_suffix}"


# ==================== BOOKING CONFIRMATION ====================

class BookingConfirmation:
    """Handles booking confirmation and booking reference generation"""
    
    @staticmethod
    def generate_booking_reference() -> str:
        """Generate unique booking reference"""
        timestamp = datetime.now().strftime("%Y%m%d")
        random_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return f"BK{timestamp}{random_code}"
    
    @staticmethod
    def create_booking(flight: Dict, passengers: List[Dict], 
                      total_amount: float, transaction_id: str) -> Dict:
        """Create a complete booking record"""
        booking_ref = BookingConfirmation.generate_booking_reference()
        booking = {
            "booking_reference": booking_ref,
            "booking_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "flight": {
                "flight_id": flight['flight_id'],
                "airline": flight['airline'],
                "departure_city": flight['departure_city'],
                "arrival_city": flight['arrival_city'],
                "departure_time": flight['departure_time'],
                "arrival_time": flight['arrival_time'],
                "price_per_passenger": flight['price']
            },
            "passengers": passengers,
            "total_passengers": len(passengers),
            "total_amount": total_amount,
            "transaction_id": transaction_id,
            "status": "CONFIRMED",
            "cancellation_fee": total_amount * 0.1  # 10% cancellation fee
        }
        return booking
    
    @staticmethod
    def display_confirmation(booking: Dict):
        """Display booking confirmation details"""
        print("\n" + "="*60)
        print("✈️  BOOKING CONFIRMATION".center(60))
        print("="*60)
        print(f"\n📌 Booking Reference: {booking['booking_reference']}")
        print(f"📅 Booking Date: {booking['booking_date']}")
        print(f"\n✈️  FLIGHT DETAILS:")
        print(f"   Airline: {booking['flight']['airline']}")
        print(f"   Route: {booking['flight']['departure_city']} → {booking['flight']['arrival_city']}")
        print(f"   Departure: {booking['flight']['departure_time']}")
        print(f"   Arrival: {booking['flight']['arrival_time']}")
        print(f"   Price per Passenger: ${booking['flight']['price_per_passenger']:.2f}")
        
        print(f"\n👥 PASSENGERS ({booking['total_passengers']}):")
        for i, passenger in enumerate(booking['passengers'], 1):
            print(f"   {i}. {passenger['name']} (Seat: {passenger['seat_number']})")
            print(f"      Passport: {passenger['passport']}")
        
        print(f"\n💰 PAYMENT DETAILS:")
        print(f"   Transaction ID: {booking['transaction_id']}")
        print(f"   Total Amount: ${booking['total_amount']:.2f}")
        print(f"   Cancellation Fee (10%): ${booking['cancellation_fee']:.2f}")
        print(f"   Refund Amount (if cancelled): ${booking['total_amount'] - booking['cancellation_fee']:.2f}")
        
        print(f"\n✅ Status: {booking['status']}")
        print("="*60)
        print("Thank you for booking with us! ✨")
        print("="*60 + "\n")


# ==================== BOOKING MANAGEMENT ====================

class BookingManager:
    """Manages all bookings"""
    
    def __init__(self):
        self.bookings = DataManager.load_bookings()
        self.flights = DataManager.load_flights()
    
    def add_booking(self, booking: Dict) -> bool:
        """Add a new booking"""
        self.bookings.append(booking)
        return DataManager.save_bookings(self.bookings)
    
    def find_booking(self, booking_reference: str) -> Optional[Dict]:
        """Find booking by reference"""
        for booking in self.bookings:
            if booking['booking_reference'].upper() == booking_reference.upper():
                return booking
        return None
    
    def get_bookings_by_email(self, email: str) -> List[Dict]:
        """Get all bookings for an email address"""
        results = []
        for booking in self.bookings:
            for passenger in booking['passengers']:
                if passenger['email'].lower() == email.lower():
                    results.append(booking)
                    break
        return results
    
    def cancel_booking(self, booking_reference: str, email: str) -> Tuple[bool, str]:
        """Cancel a booking with refund calculation"""
        booking = self.find_booking(booking_reference)
        
        if not booking:
            return False, "❌ Booking not found"
        
        # Verify email matches a passenger
        email_found = False
        for passenger in booking['passengers']:
            if passenger['email'].lower() == email.lower():
                email_found = True
                break
        
        if not email_found:
            return False, "❌ Email does not match booking"
        
        if booking['status'] == 'CANCELLED':
            return False, "❌ Booking is already cancelled"
        
        # Calculate refund
        refund_amount = booking['total_amount'] - booking['cancellation_fee']
        
        # Update booking status
        booking['status'] = 'CANCELLED'
        booking['cancellation_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        booking['refund_amount'] = refund_amount
        
        # Update flight seats
        flight_id = booking['flight']['flight_id']
        for flight in self.flights:
            if flight['flight_id'] == flight_id:
                flight['available_seats'] += booking['total_passengers']
                break
        
        # Save changes
        DataManager.save_bookings(self.bookings)
        DataManager.save_flights(self.flights)
        
        message = f"""✅ Booking Cancelled Successfully!
   Booking Reference: {booking_reference}
   Cancellation Fee: ${booking['cancellation_fee']:.2f}
   Refund Amount: ${refund_amount:.2f}
   Status: CANCELLED"""
        
        return True, message
    
    def update_flight_seats(self, flight_id: str, seats_to_book: int) -> bool:
        """Update available seats for a flight"""
        for flight in self.flights:
            if flight['flight_id'] == flight_id:
                if flight['available_seats'] >= seats_to_book:
                    flight['available_seats'] -= seats_to_book
                    DataManager.save_flights(self.flights)
                    return True
                return False
        return False


# ==================== MAIN FLIGHT BOOKING SYSTEM ====================

class FlightBookingSystem:
    """Main flight booking system orchestrator"""
    
    def __init__(self):
        self.search = FlightSearch(DataManager.load_flights())
        self.passengers = PassengerDetails()
        self.booking_manager = BookingManager()
        self.selected_flight: Optional[Dict] = None
    
    def display_menu(self):
        """Display main menu"""
        print("\n" + "="*60)
        print("✈️  FLIGHT BOOKING SYSTEM".center(60))
        print("="*60)
        print("""
1. Search Flights
2. Add Passenger Details
3. View Current Passengers
4. Process Payment & Book
5. View My Bookings
6. Cancel Booking
7. Exit

""")
    
    def search_flights(self):
        """Search for flights"""
        print("\n" + "-"*60)
        print("FLIGHT SEARCH".center(60))
        print("-"*60)
        
        # Get available cities
        cities = self.search.get_all_cities()
        print(f"\nAvailable cities: {', '.join(cities)}\n")
        
        # Get departure city
        while True:
            departure = input("Enter departure city: ").strip()
            if departure and departure in [c for c in cities if c.lower() == departure.lower()]:
                departure = next(c for c in cities if c.lower() == departure.lower())
                break
            print("❌ Invalid city. Please try again.")
        
        # Get arrival city
        while True:
            arrival = input("Enter arrival city: ").strip()
            if arrival and arrival in [c for c in cities if c.lower() == arrival.lower()]:
                arrival = next(c for c in cities if c.lower() == arrival.lower())
                break
            print("❌ Invalid city. Please try again.")
        
        if departure.lower() == arrival.lower():
            print("❌ Departure and arrival cities must be different")
            return
        
        # Get travel date
        while True:
            date = input("Enter travel date (YYYY-MM-DD): ").strip()
            is_valid, msg = Validator.validate_date(date)
            if is_valid:
                break
            print(f"❌ {msg}")
        
        # Search flights
        results = self.search.search(departure, arrival, date)
        
        if not results:
            print(f"\n❌ No flights found from {departure} to {arrival} on {date}")
            return
        
        # Display results
        print(f"\n✅ Found {len(results)} flight(s):\n")
        for idx, flight in enumerate(results, 1):
            print(f"{idx}. {flight['airline']}")
            print(f"   {flight['departure_city']} → {flight['arrival_city']}")
            print(f"   Departure: {flight['departure_time']}")
            print(f"   Arrival: {flight['arrival_time']}")
            print(f"   Duration: {flight['duration']}")
            print(f"   Price: ${flight['price']:.2f} per passenger")
            print(f"   Available Seats: {flight['available_seats']}")
            print()
        
        # Select flight
        while True:
            try:
                choice = int(input("Select flight number (0 to cancel): "))
                if choice == 0:
                    return
                if 1 <= choice <= len(results):
                    self.selected_flight = results[choice - 1]
                    print(f"\n✅ Flight {self.selected_flight['flight_id']} selected!")
                    return
                print("❌ Invalid selection")
            except ValueError:
                print("❌ Please enter a valid number")
    
    def add_passenger(self):
        """Add passenger details"""
        if not self.selected_flight:
            print("❌ Please select a flight first")
            return
        
        max_passengers = min(5, self.selected_flight['available_seats'])
        
        if len(self.passengers.get_passengers()) >= max_passengers:
            print(f"❌ Maximum {max_passengers} passengers allowed")
            return
        
        print(f"\n" + "-"*60)
        print(f"ADD PASSENGER ({len(self.passengers.get_passengers()) + 1}/{max_passengers})".center(60))
        print("-"*60)
        
        while True:
            name = input("Full Name: ").strip()
            is_valid, msg = Validator.validate_name(name)
            if is_valid:
                break
            print(f"❌ {msg}")
        
        while True:
            email = input("Email: ").strip()
            is_valid, msg = Validator.validate_email(email)
            if is_valid:
                break
            print(f"❌ {msg}")
        
        while True:
            phone = input("Phone Number: ").strip()
            is_valid, msg = Validator.validate_phone(phone)
            if is_valid:
                break
            print(f"❌ {msg}")
        
        while True:
            dob = input("Date of Birth (YYYY-MM-DD): ").strip()
            is_valid, msg = Validator.validate_dob(dob)
            if is_valid:
                break
            print(f"❌ {msg}")
        
        while True:
            passport = input("Passport Number: ").strip()
            is_valid, msg = Validator.validate_passport(passport)
            if is_valid:
                break
            print(f"❌ {msg}")
        
        if self.passengers.add_passenger(name, email, phone, dob, passport):
            print(f"✅ Passenger added successfully! ({len(self.passengers.get_passengers())}/{max_passengers})")
        else:
            print("❌ Failed to add passenger")
    
    def view_passengers(self):
        """View added passengers"""
        passengers = self.passengers.get_passengers()
        
        if not passengers:
            print("❌ No passengers added yet")
            return
        
        print(f"\n" + "-"*60)
        print("CURRENT PASSENGERS".center(60))
        print("-"*60)
        
        for idx, passenger in enumerate(passengers, 1):
            print(f"\n{idx}. {passenger['name']}")
            print(f"   Email: {passenger['email']}")
            print(f"   Phone: {passenger['phone']}")
            print(f"   DOB: {passenger['dob']}")
            print(f"   Passport: {passenger['passport']}")
            print(f"   Seat: {passenger['seat_number']}")
    
    def process_booking(self):
        """Complete booking with payment"""
        if not self.selected_flight:
            print("❌ Please select a flight first")
            return
        
        passengers = self.passengers.get_passengers()
        if not passengers:
            print("❌ Please add at least one passenger")
            return
        
        # Check seat availability
        if not self.booking_manager.update_flight_seats(
            self.selected_flight['flight_id'], 
            len(passengers)
        ):
            print("❌ Not enough seats available")
            return
        
        print(f"\n" + "-"*60)
        print("PAYMENT DETAILS".center(60))
        print("-"*60)
        
        # Calculate total
        total_amount = self.selected_flight['price'] * len(passengers)
        print(f"\nTotal Amount: ${total_amount:.2f}")
        print(f"Number of Passengers: {len(passengers)}")
        
        # Get payment details
        while True:
            cardholder = input("\nCardholder Name: ").strip()
            is_valid, msg = Validator.validate_name(cardholder)
            if is_valid:
                break
            print(f"❌ {msg}")
        
        while True:
            card_number = input("Card Number: ").strip()
            is_valid, msg = Validator.validate_card_number(card_number)
            if is_valid:
                break
            print(f"❌ {msg}")
        
        while True:
            expiry = input("Expiry Date (MM/YY): ").strip()
            is_valid, msg = Validator.validate_expiry(expiry)
            if is_valid:
                break
            print(f"❌ {msg}")
        
        while True:
            cvv = input("CVV: ").strip()
            is_valid, msg = Validator.validate_cvv(cvv)
            if is_valid:
                break
            print(f"❌ {msg}")
        
        # Process payment
        print("\n⏳ Processing payment...")
        success, message, transaction_id = PaymentProcessor.process_payment(
            total_amount, cardholder, card_number, expiry, cvv
        )
        
        if not success:
            print(f"❌ {message}")
            # Restore seat availability
            self.selected_flight['available_seats'] += len(passengers)
            DataManager.save_flights(self.booking_manager.flights)
            return
        
        print(f"✅ {message}")
        
        # Create booking
        booking = BookingConfirmation.create_booking(
            self.selected_flight,
            passengers,
            total_amount,
            transaction_id
        )
        
        # Save booking
        if self.booking_manager.add_booking(booking):
            BookingConfirmation.display_confirmation(booking)
            # Reset for next booking
            self.passengers.clear()
            self.selected_flight = None
        else:
            print("❌ Failed to save booking")
    
    def view_bookings(self):
        """View bookings by email"""
        print("\n" + "-"*60)
        print("VIEW MY BOOKINGS".center(60))
        print("-"*60)
        
        while True:
            email = input("\nEnter your email: ").strip()
            is_valid, msg = Validator.validate_email(email)
            if is_valid:
                break
            print(f"❌ {msg}")
        
        bookings = self.booking_manager.get_bookings_by_email(email)
        
        if not bookings:
            print(f"❌ No bookings found for {email}")
            return
        
        print(f"\n✅ Found {len(bookings)} booking(s):\n")
        
        for booking in bookings:
            status_symbol = "✅" if booking['status'] == "CONFIRMED" else "❌"
            print(f"{status_symbol} Booking Reference: {booking['booking_reference']}")
            print(f"   Flight: {booking['flight']['airline']} - {booking['flight']['departure_city']} → {booking['flight']['arrival_city']}")
            print(f"   Departure: {booking['flight']['departure_time']}")
            print(f"   Passengers: {booking['total_passengers']}")
            print(f"   Total Amount: ${booking['total_amount']:.2f}")
            print(f"   Status: {booking['status']}")
            if booking['status'] == 'CANCELLED':
                print(f"   Refund Amount: ${booking['refund_amount']:.2f}")
            print()
    
    def cancel_booking(self):
        """Cancel an existing booking"""
        print("\n" + "-"*60)
        print("CANCEL BOOKING".center(60))
        print("-"*60)
        
        while True:
            booking_ref = input("\nEnter booking reference: ").strip()
            if booking_ref:
                break
            print("❌ Booking reference cannot be empty")
        
        while True:
            email = input("Enter your email: ").strip()
            is_valid, msg = Validator.validate_email(email)
            if is_valid:
                break
            print(f"❌ {msg}")
        
        success, message = self.booking_manager.cancel_booking(booking_ref, email)
        print(f"\n{message}")
    
    def run(self):
        """Run the flight booking system"""
        while True:
            self.display_menu()
            choice = input("Select an option (1-7): ").strip()
            
            if choice == '1':
                self.search_flights()
            elif choice == '2':
                self.add_passenger()
            elif choice == '3':
                self.view_passengers()
            elif choice == '4':
                self.process_booking()
            elif choice == '5':
                self.view_bookings()
            elif choice == '6':
                self.cancel_booking()
            elif choice == '7':
                print("\n👋 Thank you for using Flight Booking System. Goodbye!")
                break
            else:
                print("❌ Invalid option. Please try again.")


# ==================== ENTRY POINT ====================

if __name__ == "__main__":
    print("🚀 Initializing Flight Booking System...")
    system = FlightBookingSystem()
    system.run()
