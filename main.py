import json
import os
from datetime import datetime
import re

# Sample flight data
FLIGHTS = [
    {"id": "PK701", "from": "Karachi", "to": "Dubai", "time": "08:00", "price": 200, "seats": 180},
    {"id": "EK603", "from": "Karachi", "to": "Lahore", "time": "10:00", "price": 150, "seats": 150},
    {"id": "QR607", "from": "Islamabad", "to": "Dubai", "time": "14:00", "price": 250, "seats": 120},
    {"id": "PK702", "from": "Dubai", "to": "Karachi", "time": "11:00", "price": 220, "seats": 160},
    {"id": "EK604", "from": "Lahore", "to": "Dubai", "time": "16:00", "price": 270, "seats": 140},
]

BOOKINGS_FILE = "bookings.json"

def load_bookings():
    """Load bookings from JSON file"""
    if os.path.exists(BOOKINGS_FILE):
        try:
            with open(BOOKINGS_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def save_bookings(bookings):
    """Save bookings to JSON file"""
    try:
        with open(BOOKINGS_FILE, "w") as f:
            json.dump(bookings, f, indent=4)
        return True
    except IOError as e:
        print(f"❌ Error saving bookings: {e}")
        return False

def validate_date(date_str):
    """Validate date format YYYY-MM-DD"""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def validate_email(email):
    """Validate email format"""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None

def validate_passport(passport):
    """Validate passport format (6-9 alphanumeric characters)"""
    return len(passport) >= 6 and len(passport) <= 9 and passport.isalnum()

def validate_card_number(card_num):
    """Validate card number (16 digits)"""
    return card_num.isdigit() and len(card_num) == 16

def validate_cvv(cvv):
    """Validate CVV (3 digits)"""
    return cvv.isdigit() and len(cvv) == 3

def validate_seat(seat):
    """Validate seat format (A1-F30)"""
    if len(seat) < 2 or len(seat) > 3:
        return False
    if seat[0].upper() not in ['A', 'B', 'C', 'D', 'E', 'F']:
        return False
    if not seat[1:].isdigit():
        return False
    seat_num = int(seat[1:])
    return 1 <= seat_num <= 30

def search_flights():
    """Search flights with user input"""
    print("\n" + "="*50)
    print("🔍 FLIGHT SEARCH")
    print("="*50)
    
    # Get departure city
    while True:
        departure = input("Enter departure city: ").strip().title()
        if not departure:
            print("❌ Departure city cannot be empty!")
            continue
        break
    
    # Get destination city
    while True:
        destination = input("Enter destination city: ").strip().title()
        if not destination:
            print("❌ Destination city cannot be empty!")
            continue
        if destination == departure:
            print("❌ Destination cannot be the same as departure!")
            continue
        break
    
    # Get travel date
    while True:
        date_str = input("Enter travel date (YYYY-MM-DD): ").strip()
        if not validate_date(date_str):
            print("❌ Invalid date format! Use YYYY-MM-DD")
            continue
        break
    
    # Search matching flights
    matching_flights = [f for f in FLIGHTS if f["from"] == departure and f["to"] == destination]
    
    if not matching_flights:
        print(f"\n❌ No flights found from {departure} to {destination}")
        return None
    
    print(f"\n✅ Found {len(matching_flights)} flight(s):\n")
    for idx, flight in enumerate(matching_flights, 1):
        print(f"{idx}. {flight['id']} - {flight['from']} to {flight['to']}")
        print(f"   Time: {flight['time']} | Price: ${flight['price']} | Seats: {flight['seats']}")
    
    # Select flight
    while True:
        selection = input(f"\nSelect flight (1-{len(matching_flights)}): ").strip()
        if selection.isdigit() and 1 <= int(selection) <= len(matching_flights):
            selected_flight = matching_flights[int(selection) - 1].copy()
            selected_flight["date"] = date_str
            return selected_flight
        else:
            print(f"❌ Invalid selection! Enter 1-{len(matching_flights)}")

def book_flight():
    """Complete booking process"""
    print("\n" + "="*50)
    print("🎫 FLIGHT BOOKING")
    print("="*50)
    
    # Search for flight
    selected_flight = search_flights()
    if not selected_flight:
        return
    
    # Get passenger details
    print("\n" + "="*50)
    print("👤 PASSENGER DETAILS")
    print("="*50)
    
    # Passenger name
    while True:
        passenger_name = input("Enter passenger name: ").strip()
        if not passenger_name or not all(c.isalpha() or c.isspace() for c in passenger_name):
            print("❌ Invalid name! Use only letters and spaces")
            continue
        break
    
    # Passport number
    while True:
        passport = input("Enter passport number: ").strip().upper()
        if not validate_passport(passport):
            print("❌ Invalid passport! Use 6-9 alphanumeric characters")
            continue
        break
    
    # Email
    while True:
        email = input("Enter email address: ").strip()
        if not validate_email(email):
            print("❌ Invalid email format!")
            continue
        break
    
    # Seat selection
    while True:
        seat = input("Select seat (A1-F30): ").strip().upper()
        if not validate_seat(seat):
            print("❌ Invalid seat! Use format like A1, B12, F30")
            continue
        break
    
    # Payment processing
    print("\n" + "="*50)
    print("💳 PAYMENT PROCESSING")
    print("="*50)
    
    total_amount = selected_flight["price"]
    print(f"Total amount: ${total_amount}")
    
    print("\nSelect payment method:")
    print("1. Credit Card")
    print("2. Debit Card")
    print("3. PayPal")
    
    payment_method = None
    while True:
        choice = input("Enter choice (1-3): ").strip()
        if choice == "1":
            payment_method = "Credit Card"
            break
        elif choice == "2":
            payment_method = "Debit Card"
            break
        elif choice == "3":
            payment_method = "PayPal"
            break
        else:
            print("❌ Invalid choice! Enter 1-3")
    
    # Process payment based on method
    if payment_method == "PayPal":
        while True:
            email_paypal = input("Enter PayPal email: ").strip()
            if not validate_email(email_paypal):
                print("❌ Invalid email format!")
                continue
            break
    else:
        # Credit/Debit card details
        while True:
            card_number = input("Enter card number (16 digits): ").strip()
            if not validate_card_number(card_number):
                print("❌ Invalid card number! Use 16 digits")
                continue
            break
        
        while True:
            expiry = input("Enter expiry (MM/YY): ").strip()
            if not re.match(r"^\d{2}/\d{2}$", expiry):
                print("❌ Invalid format! Use MM/YY")
                continue
            break
        
        while True:
            cvv = input("Enter CVV (3 digits): ").strip()
            if not validate_cvv(cvv):
                print("❌ Invalid CVV! Use 3 digits")
                continue
            break
    
    # Process payment
    print("\n⏳ Processing payment...")
    payment_status = "Completed"
    print("✅ Payment successful!")
    
    # Generate booking ID
    booking_id = f"BK{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # Create booking record
    booking = {
        "booking_id": booking_id,
        "passenger": passenger_name,
        "passport": passport,
        "email": email,
        "flight_id": selected_flight["id"],
        "from": selected_flight["from"],
        "to": selected_flight["to"],
        "date": selected_flight["date"],
        "time": selected_flight["time"],
        "seat": seat,
        "price": total_amount,
        "payment_method": payment_method,
        "payment_status": payment_status,
        "booking_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Save booking
    bookings = load_bookings()
    bookings.append(booking)
    if save_bookings(bookings):
        print("\n" + "="*50)
        print("✅ BOOKING CONFIRMED!")
        print("="*50)
        print(f"Booking ID: {booking_id}")
        print(f"Passenger: {passenger_name}")
        print(f"Flight: {selected_flight['id']} - {selected_flight['from']} to {selected_flight['to']}")
        print(f"Date & Time: {selected_flight['date']} {selected_flight['time']}")
        print(f"Seat: {seat}")
        print(f"Total: ${total_amount}")
        print(f"Confirmation email sent to: {email}")
        print("="*50)
    else:
        print("❌ Failed to save booking!")

def view_bookings():
    """View all user bookings"""
    print("\n" + "="*50)
    print("📋 MY BOOKINGS")
    print("="*50)
    
    bookings = load_bookings()
    
    if not bookings:
        print("❌ No bookings found!")
        return
    
    for idx, booking in enumerate(bookings, 1):
        print(f"\n{idx}. Booking ID: {booking['booking_id']}")
        print(f"   Passenger: {booking['passenger']}")
        print(f"   Flight: {booking['flight_id']} - {booking['from']} to {booking['to']}")
        print(f"   Date & Time: {booking['date']} {booking['time']}")
        print(f"   Seat: {booking['seat']}")
        print(f"   Total: ${booking['price']}")
        print(f"   Status: {booking['payment_status']}")

def cancel_booking():
    """Cancel a booking"""
    print("\n" + "="*50)
    print("❌ CANCEL BOOKING")
    print("="*50)
    
    bookings = load_bookings()
    
    if not bookings:
        print("❌ No bookings found to cancel!")
        return
    
    print("\nYour bookings:\n")
    for idx, booking in enumerate(bookings, 1):
        print(f"{idx}. {booking['booking_id']} - {booking['flight_id']} ({booking['date']})")
    
    while True:
        choice = input(f"\nSelect booking to cancel (1-{len(bookings)}) or 0 to exit: ").strip()
        if choice == "0":
            return
        if choice.isdigit() and 1 <= int(choice) <= len(bookings):
            booking_index = int(choice) - 1
            cancelled_booking = bookings.pop(booking_index)
            
            if save_bookings(bookings):
                print(f"\n✅ Booking {cancelled_booking['booking_id']} cancelled successfully!")
                print(f"Refund of ${cancelled_booking['price']} will be processed to your original payment method.")
            else:
                print("❌ Failed to cancel booking!")
            break
        else:
            print(f"❌ Invalid choice! Enter 1-{len(bookings)} or 0")

def main():
    """Main application loop"""
    print("\n" + "="*50)
    print("✈️ WELCOME TO FLIGHT BOOKING SYSTEM ✈️")
    print("="*50)
    
    while True:
        print("\n" + "="*50)
        print("MAIN MENU")
        print("="*50)
        print("1. Search & Book Flight")
        print("2. View My Bookings")
        print("3. Cancel Booking")
        print("4. Exit")
        print("="*50)
        
        choice = input("Enter choice (1-4): ").strip()
        
        if choice == "1":
            book_flight()
        elif choice == "2":
            view_bookings()
        elif choice == "3":
            cancel_booking()
        elif choice == "4":
            print("\n🙏 Thank you for using Flight Booking System! ✈️")
            print("Safe travels!\n")
            break
        else:
            print("❌ Invalid choice! Please enter 1-4")

if __name__ == "__main__":
    main()
