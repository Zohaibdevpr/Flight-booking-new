#!/usr/bin/env python3
"""
Interactive Flight Booking System
A comprehensive flight booking application with flight search, booking, payment processing,
and JSON data persistence with comprehensive input validation and error handling.
"""

import json
import os
import re
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from enum import Enum
import hashlib


class BookingStatus(Enum):
    """Enumeration for booking statuses"""
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"


class PaymentMethod(Enum):
    """Enumeration for payment methods"""
    CREDIT_CARD = "CREDIT_CARD"
    DEBIT_CARD = "DEBIT_CARD"
    PAYPAL = "PAYPAL"
    BANK_TRANSFER = "BANK_TRANSFER"


class Database:
    """Handles JSON data persistence"""
    
    def __init__(self, data_dir: str = "data"):
        """Initialize database with specified directory"""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        self.flights_file = self.data_dir / "flights.json"
        self.bookings_file = self.data_dir / "bookings.json"
        self.users_file = self.data_dir / "users.json"
        self.payments_file = self.data_dir / "payments.json"
        
        self._initialize_data()
    
    def _initialize_data(self):
        """Initialize data files if they don't exist"""
        if not self.flights_file.exists():
            self._create_sample_flights()
        
        if not self.bookings_file.exists():
            self._write_json(self.bookings_file, [])
        
        if not self.users_file.exists():
            self._write_json(self.users_file, [])
        
        if not self.payments_file.exists():
            self._write_json(self.payments_file, [])
    
    def _create_sample_flights(self):
        """Create sample flight data"""
        sample_flights = [
            {
                "id": "FL001",
                "airline": "Sky Airways",
                "departure_city": "New York",
                "arrival_city": "Los Angeles",
                "departure_time": "2025-12-25 08:00:00",
                "arrival_time": "2025-12-25 11:30:00",
                "duration_minutes": 330,
                "price": 299.99,
                "available_seats": 150,
                "total_seats": 180,
                "aircraft": "Boeing 737"
            },
            {
                "id": "FL002",
                "airline": "Global Air",
                "departure_city": "New York",
                "arrival_city": "Los Angeles",
                "departure_time": "2025-12-25 14:00:00",
                "arrival_time": "2025-12-25 17:45:00",
                "duration_minutes": 345,
                "price": 279.99,
                "available_seats": 45,
                "total_seats": 180,
                "aircraft": "Airbus A320"
            },
            {
                "id": "FL003",
                "airline": "Sky Airways",
                "departure_city": "New York",
                "arrival_city": "Miami",
                "departure_time": "2025-12-25 10:30:00",
                "arrival_time": "2025-12-25 13:15:00",
                "duration_minutes": 165,
                "price": 199.99,
                "available_seats": 75,
                "total_seats": 150,
                "aircraft": "Boeing 737"
            },
            {
                "id": "FL004",
                "airline": "Premium Airlines",
                "departure_city": "Los Angeles",
                "arrival_city": "Chicago",
                "departure_time": "2025-12-26 09:00:00",
                "arrival_time": "2025-12-26 16:30:00",
                "duration_minutes": 330,
                "price": 349.99,
                "available_seats": 20,
                "total_seats": 180,
                "aircraft": "Boeing 777"
            },
            {
                "id": "FL005",
                "airline": "Budget Airlines",
                "departure_city": "Los Angeles",
                "arrival_city": "Chicago",
                "departure_time": "2025-12-26 18:00:00",
                "arrival_time": "2025-12-27 01:30:00",
                "duration_minutes": 330,
                "price": 149.99,
                "available_seats": 120,
                "total_seats": 150,
                "aircraft": "Airbus A319"
            }
        ]
        self._write_json(self.flights_file, sample_flights)
    
    def _read_json(self, filepath: Path) -> List[Dict]:
        """Read JSON file safely"""
        try:
            if filepath.exists():
                with open(filepath, 'r') as f:
                    return json.load(f)
            return []
        except json.JSONDecodeError:
            print(f"Error: Corrupted JSON file at {filepath}")
            return []
    
    def _write_json(self, filepath: Path, data):
        """Write JSON file safely"""
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            raise Exception(f"Error writing to {filepath}: {str(e)}")
    
    def get_all_flights(self) -> List[Dict]:
        """Retrieve all flights"""
        return self._read_json(self.flights_file)
    
    def get_flight_by_id(self, flight_id: str) -> Optional[Dict]:
        """Retrieve a specific flight"""
        flights = self.get_all_flights()
        return next((f for f in flights if f["id"] == flight_id), None)
    
    def update_flight(self, flight_id: str, updates: Dict):
        """Update flight information"""
        flights = self.get_all_flights()
        for flight in flights:
            if flight["id"] == flight_id:
                flight.update(updates)
                self._write_json(self.flights_file, flights)
                return True
        return False
    
    def save_booking(self, booking: Dict) -> bool:
        """Save a new booking"""
        bookings = self._read_json(self.bookings_file)
        bookings.append(booking)
        self._write_json(self.bookings_file, bookings)
        return True
    
    def get_booking_by_id(self, booking_id: str) -> Optional[Dict]:
        """Retrieve a specific booking"""
        bookings = self._read_json(self.bookings_file)
        return next((b for b in bookings if b["id"] == booking_id), None)
    
    def update_booking(self, booking_id: str, updates: Dict) -> bool:
        """Update booking information"""
        bookings = self._read_json(self.bookings_file)
        for booking in bookings:
            if booking["id"] == booking_id:
                booking.update(updates)
                self._write_json(self.bookings_file, bookings)
                return True
        return False
    
    def get_user_bookings(self, email: str) -> List[Dict]:
        """Retrieve all bookings for a user"""
        bookings = self._read_json(self.bookings_file)
        return [b for b in bookings if b.get("passenger_email") == email]
    
    def save_payment(self, payment: Dict) -> bool:
        """Save payment record"""
        payments = self._read_json(self.payments_file)
        payments.append(payment)
        self._write_json(self.payments_file, payments)
        return True
    
    def get_payment_by_booking_id(self, booking_id: str) -> Optional[Dict]:
        """Retrieve payment for a booking"""
        payments = self._read_json(self.payments_file)
        return next((p for p in payments if p["booking_id"] == booking_id), None)


class Validator:
    """Input validation utilities"""
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, email):
            return True, ""
        return False, "Invalid email format"
    
    @staticmethod
    def validate_phone(phone: str) -> Tuple[bool, str]:
        """Validate phone number"""
        phone = phone.replace("-", "").replace(" ", "").replace("(", "").replace(")", "")
        if len(phone) < 10 or len(phone) > 15 or not phone.isdigit():
            return False, "Phone number must be 10-15 digits"
        return True, ""
    
    @staticmethod
    def validate_name(name: str) -> Tuple[bool, str]:
        """Validate passenger name"""
        if len(name.strip()) < 2:
            return False, "Name must be at least 2 characters long"
        if not all(c.isalpha() or c.isspace() for c in name):
            return False, "Name can only contain letters and spaces"
        return True, ""
    
    @staticmethod
    def validate_date(date_str: str) -> Tuple[bool, str]:
        """Validate date format (YYYY-MM-DD)"""
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True, ""
        except ValueError:
            return False, "Invalid date format. Use YYYY-MM-DD"
    
    @staticmethod
    def validate_credit_card(card_number: str) -> Tuple[bool, str]:
        """Validate credit card using Luhn algorithm"""
        card_number = card_number.replace(" ", "").replace("-", "")
        
        if not card_number.isdigit() or len(card_number) < 13 or len(card_number) > 19:
            return False, "Invalid card number length"
        
        # Luhn algorithm
        total = 0
        for i, digit in enumerate(reversed(card_number)):
            n = int(digit)
            if i % 2 == 1:
                n *= 2
                if n > 9:
                    n -= 9
            total += n
        
        if total % 10 != 0:
            return False, "Invalid card number (failed Luhn check)"
        
        return True, ""
    
    @staticmethod
    def validate_cvv(cvv: str) -> Tuple[bool, str]:
        """Validate CVV"""
        if not cvv.isdigit() or len(cvv) < 3 or len(cvv) > 4:
            return False, "CVV must be 3-4 digits"
        return True, ""
    
    @staticmethod
    def validate_expiry(expiry_date: str) -> Tuple[bool, str]:
        """Validate card expiry date (MM/YY)"""
        try:
            month, year = expiry_date.split("/")
            month = int(month)
            year = int(year)
            
            if month < 1 or month > 12:
                return False, "Invalid month"
            
            current_date = datetime.now()
            current_year = current_date.year % 100
            
            if year < current_year or (year == current_year and month < current_date.month):
                return False, "Card has expired"
            
            return True, ""
        except (ValueError, IndexError):
            return False, "Invalid expiry format. Use MM/YY"


class PaymentProcessor:
    """Handles payment processing"""
    
    def __init__(self, database: Database):
        self.database = database
        self.validator = Validator()
    
    def process_payment(self, booking_id: str, amount: float, payment_method: str,
                       card_details: Optional[Dict] = None) -> Tuple[bool, str, Optional[str]]:
        """
        Process payment for a booking
        Returns: (success, message, transaction_id)
        """
        try:
            # Validate amount
            if amount <= 0:
                return False, "Invalid amount", None
            
            payment_method_obj = PaymentMethod[payment_method.upper()]
            
            # Process based on payment method
            if payment_method_obj == PaymentMethod.CREDIT_CARD or payment_method_obj == PaymentMethod.DEBIT_CARD:
                success, msg = self._process_card_payment(card_details)
                if not success:
                    return False, msg, None
            elif payment_method_obj == PaymentMethod.PAYPAL:
                success, msg = self._process_paypal_payment(card_details)
                if not success:
                    return False, msg, None
            elif payment_method_obj == PaymentMethod.BANK_TRANSFER:
                success, msg = self._process_bank_transfer(card_details)
                if not success:
                    return False, msg, None
            
            # Generate transaction ID
            transaction_id = str(uuid.uuid4())[:8].upper()
            
            # Save payment record
            payment_record = {
                "booking_id": booking_id,
                "amount": amount,
                "payment_method": payment_method,
                "transaction_id": transaction_id,
                "status": "COMPLETED",
                "timestamp": datetime.now().isoformat(),
                "card_last_four": card_details.get("card_number", "")[-4:] if card_details else "N/A"
            }
            
            self.database.save_payment(payment_record)
            
            return True, f"Payment processed successfully. Transaction ID: {transaction_id}", transaction_id
        
        except KeyError:
            return False, "Invalid payment method", None
        except Exception as e:
            return False, f"Payment processing error: {str(e)}", None
    
    def _process_card_payment(self, card_details: Dict) -> Tuple[bool, str]:
        """Process credit/debit card payment"""
        if not card_details:
            return False, "Card details required"
        
        # Validate card number
        valid, msg = self.validator.validate_credit_card(card_details.get("card_number", ""))
        if not valid:
            return False, msg
        
        # Validate CVV
        valid, msg = self.validator.validate_cvv(card_details.get("cvv", ""))
        if not valid:
            return False, msg
        
        # Validate expiry
        valid, msg = self.validator.validate_expiry(card_details.get("expiry_date", ""))
        if not valid:
            return False, msg
        
        # Simulate payment processing
        import random
        if random.random() > 0.95:  # 5% failure rate simulation
            return False, "Card declined by issuer"
        
        return True, "Card payment successful"
    
    def _process_paypal_payment(self, paypal_details: Dict) -> Tuple[bool, str]:
        """Process PayPal payment"""
        if not paypal_details or "email" not in paypal_details:
            return False, "PayPal email required"
        
        valid, msg = self.validator.validate_email(paypal_details["email"])
        if not valid:
            return False, "Invalid PayPal email"
        
        import random
        if random.random() > 0.98:
            return False, "PayPal payment failed"
        
        return True, "PayPal payment successful"
    
    def _process_bank_transfer(self, bank_details: Dict) -> Tuple[bool, str]:
        """Process bank transfer"""
        if not bank_details or "account_number" not in bank_details:
            return False, "Bank account details required"
        
        if not bank_details["account_number"].replace(" ", "").isdigit():
            return False, "Invalid account number"
        
        return True, "Bank transfer initiated successfully"


class FlightBookingSystem:
    """Main flight booking system"""
    
    def __init__(self):
        self.database = Database()
        self.payment_processor = PaymentProcessor(self.database)
        self.validator = Validator()
        self.current_user = None
    
    def search_flights(self, departure: str, arrival: str, date: str) -> List[Dict]:
        """
        Search for available flights
        Returns list of matching flights
        """
        try:
            # Validate date
            valid, msg = self.validator.validate_date(date)
            if not valid:
                print(f"Error: {msg}")
                return []
            
            # Normalize city names
            departure = departure.strip().title()
            arrival = arrival.strip().title()
            
            if departure == arrival:
                print("Error: Departure and arrival cities must be different")
                return []
            
            all_flights = self.database.get_all_flights()
            
            # Filter flights
            matching_flights = [
                f for f in all_flights
                if f["departure_city"].title() == departure and
                   f["arrival_city"].title() == arrival and
                   f["available_seats"] > 0 and
                   f["departure_time"].startswith(date)
            ]
            
            return matching_flights
        
        except Exception as e:
            print(f"Search error: {str(e)}")
            return []
    
    def display_flights(self, flights: List[Dict]):
        """Display flights in a formatted table"""
        if not flights:
            print("No flights found matching your criteria.")
            return
        
        print("\n" + "="*120)
        print(f"{'Flight ID':<12} {'Airline':<20} {'Departure':<25} {'Arrival':<25} {'Duration':<12} {'Price':<10} {'Seats':<8}")
        print("="*120)
        
        for flight in flights:
            print(f"{flight['id']:<12} {flight['airline']:<20} {flight['departure_time']:<25} "
                  f"{flight['arrival_time']:<25} {flight['duration_minutes']//60}h{flight['duration_minutes']%60}m{'':<4} "
                  f"${flight['price']:<9.2f} {flight['available_seats']:<8}")
        
        print("="*120 + "\n")
    
    def get_flight_details(self, flight_id: str) -> Optional[Dict]:
        """Get detailed information about a flight"""
        flight = self.database.get_flight_by_id(flight_id)
        
        if flight:
            print("\n" + "="*60)
            print("FLIGHT DETAILS")
            print("="*60)
            for key, value in flight.items():
                if key == "duration_minutes":
                    hours = value // 60
                    minutes = value % 60
                    print(f"{key.replace('_', ' ').title():<25}: {hours}h {minutes}m")
                elif key == "price":
                    print(f"{key.replace('_', ' ').title():<25}: ${value:.2f}")
                else:
                    print(f"{key.replace('_', ' ').title():<25}: {value}")
            print("="*60 + "\n")
        
        return flight
    
    def create_booking(self, flight_id: str, passenger_name: str, passenger_email: str,
                      passenger_phone: str, num_passengers: int) -> Optional[str]:
        """
        Create a new booking
        Returns booking ID if successful
        """
        try:
            # Validate inputs
            valid, msg = self.validator.validate_name(passenger_name)
            if not valid:
                print(f"Error: {msg}")
                return None
            
            valid, msg = self.validator.validate_email(passenger_email)
            if not valid:
                print(f"Error: {msg}")
                return None
            
            valid, msg = self.validator.validate_phone(passenger_phone)
            if not valid:
                print(f"Error: {msg}")
                return None
            
            if num_passengers < 1 or num_passengers > 9:
                print("Error: Number of passengers must be between 1 and 9")
                return None
            
            # Check flight availability
            flight = self.database.get_flight_by_id(flight_id)
            if not flight:
                print("Error: Flight not found")
                return None
            
            if flight["available_seats"] < num_passengers:
                print(f"Error: Only {flight['available_seats']} seats available")
                return None
            
            # Create booking
            booking_id = str(uuid.uuid4())[:8].upper()
            total_price = flight["price"] * num_passengers
            
            booking = {
                "id": booking_id,
                "flight_id": flight_id,
                "passenger_name": passenger_name,
                "passenger_email": passenger_email,
                "passenger_phone": passenger_phone,
                "num_passengers": num_passengers,
                "total_price": total_price,
                "status": BookingStatus.PENDING.value,
                "booking_date": datetime.now().isoformat(),
                "confirmation_number": hashlib.md5(booking_id.encode()).hexdigest()[:12].upper()
            }
            
            # Save booking
            self.database.save_booking(booking)
            
            # Update available seats
            self.database.update_flight(flight_id, {
                "available_seats": flight["available_seats"] - num_passengers
            })
            
            print(f"\nBooking created successfully!")
            print(f"Booking ID: {booking_id}")
            print(f"Confirmation Number: {booking['confirmation_number']}")
            print(f"Total Price: ${total_price:.2f}")
            
            return booking_id
        
        except Exception as e:
            print(f"Booking error: {str(e)}")
            return None
    
    def process_booking_payment(self, booking_id: str, payment_method: str) -> Tuple[bool, str]:
        """
        Process payment for a booking
        Returns: (success, message)
        """
        try:
            # Get booking
            booking = self.database.get_booking_by_id(booking_id)
            if not booking:
                return False, "Booking not found"
            
            if booking["status"] != BookingStatus.PENDING.value:
                return False, f"Booking status is {booking['status']}, cannot process payment"
            
            amount = booking["total_price"]
            
            # Get payment details based on method
            card_details = self._get_payment_details(payment_method)
            if not card_details:
                return False, "Payment cancelled"
            
            # Process payment
            success, msg, transaction_id = self.payment_processor.process_payment(
                booking_id, amount, payment_method, card_details
            )
            
            if success:
                # Update booking status
                self.database.update_booking(booking_id, {
                    "status": BookingStatus.CONFIRMED.value,
                    "transaction_id": transaction_id
                })
                
                # Display confirmation
                self._display_booking_confirmation(booking, transaction_id)
                return True, msg
            else:
                return False, msg
        
        except Exception as e:
            return False, f"Payment error: {str(e)}"
    
    def _get_payment_details(self, payment_method: str) -> Optional[Dict]:
        """Get payment details from user"""
        print("\n" + "="*60)
        print("PAYMENT DETAILS")
        print("="*60)
        
        try:
            payment_method = PaymentMethod[payment_method.upper()]
            
            if payment_method == PaymentMethod.CREDIT_CARD or payment_method == PaymentMethod.DEBIT_CARD:
                print("Enter Credit Card Details:")
                
                while True:
                    card_number = input("Card Number (16 digits): ").strip()
                    valid, msg = self.validator.validate_credit_card(card_number)
                    if valid:
                        break
                    print(f"Invalid: {msg}. Please try again.")
                
                while True:
                    cardholder_name = input("Cardholder Name: ").strip()
                    valid, msg = self.validator.validate_name(cardholder_name)
                    if valid:
                        break
                    print(f"Invalid: {msg}. Please try again.")
                
                while True:
                    expiry_date = input("Expiry Date (MM/YY): ").strip()
                    valid, msg = self.validator.validate_expiry(expiry_date)
                    if valid:
                        break
                    print(f"Invalid: {msg}. Please try again.")
                
                while True:
                    cvv = input("CVV (3-4 digits): ").strip()
                    valid, msg = self.validator.validate_cvv(cvv)
                    if valid:
                        break
                    print(f"Invalid: {msg}. Please try again.")
                
                return {
                    "card_number": card_number,
                    "cardholder_name": cardholder_name,
                    "expiry_date": expiry_date,
                    "cvv": cvv
                }
            
            elif payment_method == PaymentMethod.PAYPAL:
                print("PayPal Payment:")
                
                while True:
                    email = input("PayPal Email: ").strip()
                    valid, msg = self.validator.validate_email(email)
                    if valid:
                        break
                    print(f"Invalid: {msg}. Please try again.")
                
                return {"email": email}
            
            elif payment_method == PaymentMethod.BANK_TRANSFER:
                print("Bank Transfer Details:")
                account_number = input("Account Number: ").strip()
                routing_number = input("Routing Number: ").strip()
                
                return {
                    "account_number": account_number,
                    "routing_number": routing_number
                }
        
        except KeyError:
            print("Invalid payment method")
            return None
        except KeyboardInterrupt:
            print("\nPayment cancelled")
            return None
    
    def _display_booking_confirmation(self, booking: Dict, transaction_id: str):
        """Display booking confirmation"""
        flight = self.database.get_flight_by_id(booking["flight_id"])
        
        print("\n" + "="*70)
        print("BOOKING CONFIRMATION".center(70))
        print("="*70)
        print(f"Confirmation Number: {booking['confirmation_number']}")
        print(f"Booking ID: {booking['id']}")
        print(f"Transaction ID: {transaction_id}")
        print(f"Status: {booking['status']}")
        print("-"*70)
        print(f"Passenger Name: {booking['passenger_name']}")
        print(f"Email: {booking['passenger_email']}")
        print(f"Phone: {booking['passenger_phone']}")
        print(f"Number of Passengers: {booking['num_passengers']}")
        print("-"*70)
        print(f"Flight: {flight['airline']}")
        print(f"Route: {flight['departure_city']} → {flight['arrival_city']}")
        print(f"Departure: {flight['departure_time']}")
        print(f"Arrival: {flight['arrival_time']}")
        print(f"Aircraft: {flight['aircraft']}")
        print("-"*70)
        print(f"Total Amount Paid: ${booking['total_price']:.2f}")
        print(f"Booking Date: {booking['booking_date']}")
        print("="*70)
        print("\nA confirmation email has been sent to your email address.")
        print("Please arrive at the airport 2 hours before departure.\n")
    
    def view_booking(self, booking_id: str) -> bool:
        """View booking details"""
        booking = self.database.get_booking_by_id(booking_id)
        
        if not booking:
            print("Booking not found")
            return False
        
        flight = self.database.get_flight_by_id(booking["flight_id"])
        payment = self.database.get_payment_by_booking_id(booking_id)
        
        print("\n" + "="*70)
        print("BOOKING DETAILS".center(70))
        print("="*70)
        print(f"Booking ID: {booking['id']}")
        print(f"Confirmation Number: {booking['confirmation_number']}")
        print(f"Status: {booking['status']}")
        print("-"*70)
        print(f"Passenger: {booking['passenger_name']}")
        print(f"Email: {booking['passenger_email']}")
        print(f"Phone: {booking['passenger_phone']}")
        print(f"Number of Passengers: {booking['num_passengers']}")
        print("-"*70)
        print(f"Flight: {flight['airline']} ({flight['id']})")
        print(f"From: {flight['departure_city']} ({flight['departure_time']})")
        print(f"To: {flight['arrival_city']} ({flight['arrival_time']})")
        print(f"Aircraft: {flight['aircraft']}")
        print("-"*70)
        
        if payment:
            print(f"Payment Method: {payment['payment_method']}")
            print(f"Transaction ID: {payment['transaction_id']}")
            print(f"Card Last 4: {payment['card_last_four']}")
        
        print(f"Total Price: ${booking['total_price']:.2f}")
        print(f"Booked On: {booking['booking_date']}")
        print("="*70 + "\n")
        
        return True
    
    def cancel_booking(self, booking_id: str) -> bool:
        """Cancel a booking"""
        booking = self.database.get_booking_by_id(booking_id)
        
        if not booking:
            print("Booking not found")
            return False
        
        if booking["status"] == BookingStatus.CANCELLED.value:
            print("Booking is already cancelled")
            return False
        
        # Refund logic
        refund_amount = booking["total_price"] * 0.8  # 20% cancellation fee
        
        # Update booking
        self.database.update_booking(booking_id, {
            "status": BookingStatus.CANCELLED.value,
            "cancellation_date": datetime.now().isoformat(),
            "refund_amount": refund_amount
        })
        
        # Restore seats
        flight = self.database.get_flight_by_id(booking["flight_id"])
        self.database.update_flight(booking["flight_id"], {
            "available_seats": flight["available_seats"] + booking["num_passengers"]
        })
        
        print(f"\nBooking {booking_id} cancelled successfully!")
        print(f"Refund Amount: ${refund_amount:.2f} (20% cancellation fee applied)")
        print("Refund will be processed within 5-7 business days.\n")
        
        return True
    
    def run_interactive(self):
        """Run the interactive booking system"""
        print("\n" + "="*70)
        print("WELCOME TO FLIGHT BOOKING SYSTEM".center(70))
        print("="*70 + "\n")
        
        while True:
            print("\n" + "-"*70)
            print("MAIN MENU")
            print("-"*70)
            print("1. Search Flights")
            print("2. View Flight Details")
            print("3. Book a Flight")
            print("4. Make Payment")
            print("5. View Booking")
            print("6. Cancel Booking")
            print("7. Exit")
            print("-"*70)
            
            choice = input("Enter your choice (1-7): ").strip()
            
            if choice == "1":
                self._search_menu()
            elif choice == "2":
                self._flight_details_menu()
            elif choice == "3":
                self._booking_menu()
            elif choice == "4":
                self._payment_menu()
            elif choice == "5":
                self._view_booking_menu()
            elif choice == "6":
                self._cancel_booking_menu()
            elif choice == "7":
                print("\nThank you for using Flight Booking System. Goodbye!\n")
                break
            else:
                print("Invalid choice. Please try again.")
    
    def _search_menu(self):
        """Flight search menu"""
        print("\n" + "-"*70)
        print("FLIGHT SEARCH")
        print("-"*70)
        
        try:
            departure = input("Departure City: ").strip()
            arrival = input("Arrival City: ").strip()
            date = input("Travel Date (YYYY-MM-DD): ").strip()
            
            flights = self.search_flights(departure, arrival, date)
            
            if flights:
                print(f"\nFound {len(flights)} flight(s):")
                self.display_flights(flights)
            else:
                print("No flights found.")
        
        except KeyboardInterrupt:
            print("\nSearch cancelled")
        except Exception as e:
            print(f"Error: {str(e)}")
    
    def _flight_details_menu(self):
        """Flight details menu"""
        print("\n" + "-"*70)
        print("VIEW FLIGHT DETAILS")
        print("-"*70)
        
        try:
            flight_id = input("Enter Flight ID: ").strip().upper()
            self.get_flight_details(flight_id)
        
        except KeyboardInterrupt:
            print("\nCancelled")
        except Exception as e:
            print(f"Error: {str(e)}")
    
    def _booking_menu(self):
        """Booking menu"""
        print("\n" + "-"*70)
        print("CREATE BOOKING")
        print("-"*70)
        
        try:
            flight_id = input("Flight ID: ").strip().upper()
            passenger_name = input("Passenger Name: ").strip()
            passenger_email = input("Passenger Email: ").strip()
            passenger_phone = input("Passenger Phone: ").strip()
            
            try:
                num_passengers = int(input("Number of Passengers: ").strip())
            except ValueError:
                print("Error: Number of passengers must be a number")
                return
            
            booking_id = self.create_booking(
                flight_id, passenger_name, passenger_email,
                passenger_phone, num_passengers
            )
            
            if booking_id:
                proceed = input("\nProceed to payment? (yes/no): ").strip().lower()
                if proceed == "yes":
                    self._process_payment_for_booking(booking_id)
        
        except KeyboardInterrupt:
            print("\nBooking cancelled")
        except Exception as e:
            print(f"Error: {str(e)}")
    
    def _payment_menu(self):
        """Payment menu"""
        print("\n" + "-"*70)
        print("PAYMENT PROCESSING")
        print("-"*70)
        
        try:
            booking_id = input("Booking ID: ").strip().upper()
            self._process_payment_for_booking(booking_id)
        
        except KeyboardInterrupt:
            print("\nCancelled")
        except Exception as e:
            print(f"Error: {str(e)}")
    
    def _process_payment_for_booking(self, booking_id: str):
        """Process payment for a specific booking"""
        booking = self.database.get_booking_by_id(booking_id)
        
        if not booking:
            print("Booking not found")
            return
        
        print(f"\nBooking Amount: ${booking['total_price']:.2f}")
        print("\nPayment Methods:")
        print("1. Credit Card")
        print("2. Debit Card")
        print("3. PayPal")
        print("4. Bank Transfer")
        
        method_choice = input("Select payment method (1-4): ").strip()
        
        method_map = {
            "1": "CREDIT_CARD",
            "2": "DEBIT_CARD",
            "3": "PAYPAL",
            "4": "BANK_TRANSFER"
        }
        
        payment_method = method_map.get(method_choice)
        
        if not payment_method:
            print("Invalid choice")
            return
        
        success, msg = self.process_booking_payment(booking_id, payment_method)
        print(f"\n{msg}")
    
    def _view_booking_menu(self):
        """View booking menu"""
        print("\n" + "-"*70)
        print("VIEW BOOKING")
        print("-"*70)
        
        try:
            booking_id = input("Enter Booking ID: ").strip().upper()
            self.view_booking(booking_id)
        
        except KeyboardInterrupt:
            print("\nCancelled")
        except Exception as e:
            print(f"Error: {str(e)}")
    
    def _cancel_booking_menu(self):
        """Cancel booking menu"""
        print("\n" + "-"*70)
        print("CANCEL BOOKING")
        print("-"*70)
        
        try:
            booking_id = input("Enter Booking ID to Cancel: ").strip().upper()
            
            # Show booking details first
            booking = self.database.get_booking_by_id(booking_id)
            if booking:
                self.view_booking(booking_id)
                confirm = input("Are you sure you want to cancel this booking? (yes/no): ").strip().lower()
                
                if confirm == "yes":
                    self.cancel_booking(booking_id)
            else:
                print("Booking not found")
        
        except KeyboardInterrupt:
            print("\nCancelled")
        except Exception as e:
            print(f"Error: {str(e)}")


def main():
    """Main entry point"""
    try:
        system = FlightBookingSystem()
        system.run_interactive()
    except KeyboardInterrupt:
        print("\n\nApplication terminated by user.")
    except Exception as e:
        print(f"\nFatal error: {str(e)}")
        raise


if __name__ == "__main__":
    main()
