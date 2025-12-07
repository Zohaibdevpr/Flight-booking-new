# Flight Booking System - Step-by-Step Guide & SOLID Principles Walkthrough

## Part 1: How to Run the Project

### Step 1: Navigate to the Project Directory

```bash
# Open your terminal/command prompt and navigate to the project
cd c:\Users\Nexgen\Flight-booking-new

# Verify you're in the right directory (you should see these files)
# You should see: src/, examples/, tests/, main.py, run_demo.py, README.md
dir
```

### Step 2: (Optional) Create a Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies (Optional - only needed for testing)

```bash
# Install pytest for running tests
pip install -r requirements.txt

# Or just install pytest
pip install pytest
```

### Step 4: Run the Project - Three Options

#### **Option A: Run the Complete Demo (RECOMMENDED FOR FIRST TIME)**

```bash
# This runs the entire Flight Booking System with all SOLID principles
python main.py
```

**What You'll See:**
- Demo 1: SRP principle with Flight, Passenger, and Booking entities
- Demo 2: OCP principle with different pricing strategies
- Demo 3: OCP principle with different seating strategies
- Demo 4: LSP principle with aircraft hierarchy
- Demo 5: ISP principle with segregated interfaces
- Demo 6: DIP principle with dependency injection
- Demo 7: Complete booking workflow

#### **Option B: Run Individual SOLID Principle Demos**

```bash
# Run specific SOLID principle demo
python run_demo.py srp    # Single Responsibility Principle
python run_demo.py ocp    # Open/Closed Principle
python run_demo.py lsp    # Liskov Substitution Principle
python run_demo.py isp    # Interface Segregation Principle
python run_demo.py dip    # Dependency Inversion Principle
```

#### **Option C: Run All SOLID Demos Together**

```bash
# This runs all 5 principle demos in sequence
python run_demo.py
```

#### **Option D: Run Tests**

```bash
# Run all tests
pytest tests/ -v

# Run only integration tests
pytest tests/test_integration.py -v
```

---

## Part 2: Understanding the Project Output

### When You Run `python main.py`

The program will show you 7 demonstrations:

#### **DEMO 1: SRP - Single Responsibility Principle**

```
======================================================================
DEMO 1: SRP - Single Responsibility Principle
======================================================================

[OK] Flight entity - Responsible for flight data and seat management:
  Flight: AA101
  Route: New York → Los Angeles
  Available seats: 50/300
  Occupancy rate: 83.3%

[OK] Passenger entity - Responsible for passenger profile:
  Passenger: John Smith
  Email: john.smith@example.com
  Profile: {'id': 'P001', 'name': 'John Smith', ...}

[OK] Each class has ONE responsibility - no mixing concerns!
```

**What This Shows:**
- Flight class only manages flight data and seats
- Passenger class only manages passenger information
- Booking class only manages booking lifecycle
- Each class has ONE reason to change

---

#### **DEMO 2: OCP - Open/Closed Principle (Pricing Strategies)**

```
======================================================================
DEMO 2: OCP - Open/Closed Principle (Pricing Strategies)
======================================================================

Base price: $ 100.00
Scenario: 2 passengers, 75.0% occupancy, 10 days to departure

[OK] STANDARD: $ 100.00/person = $ 200.00 total
  (Flat pricing with passenger type discounts)
[OK] DYNAMIC: $ 450.00/person = $ 900.00 total
  (Dynamic pricing based on occupancy and time to departure)
[OK] SEASONAL: $ 130.00/person = $ 260.00 total
  (Seasonal pricing with peak, high, and low season rates)
[OK] LOYALTY: $ 90.00/person = $ 180.00 total
  (Loyalty-based pricing with tier-dependent discounts)

[OK] New pricing strategies can be added WITHOUT modifying existing code!
```

**What This Shows:**
- Different pricing strategies produce different prices
- StandardPricing: $100 (flat)
- DynamicPricing: $450 (high because high occupancy & close to departure)
- SeasonalPricing: $130 (medium, depends on season)
- LoyaltyPricing: $90 (discount for loyal customers)
- You can add new pricing without changing existing code

---

#### **DEMO 3: OCP - Open/Closed Principle (Seating Strategies)**

```
======================================================================
DEMO 3: OCP - Open/Closed Principle (Seating Strategies)
======================================================================

Available seats: ['1A', '1B', '1C', '1D', '1E', '1F', '2A', '2B', '2C', '2D', '2E', '2F']
Allocating 4 seats for passengers using different strategies:

[OK] Sequential: ['1A', '1B', '1C', '1D']
[OK] Window Priority: ['1A', '1F', '2A', '2F']
[OK] Family Allocation: ['1A', '1B', '1C', '1D']

[OK] New seating strategies can be added WITHOUT modifying existing code!
```

**What This Shows:**
- SequentialAllocation: Assigns first available seats
- WindowPriority: Prioritizes window seats (A and F)
- FamilyAllocation: Keeps families together
- Each strategy produces different seating arrangements
- You can add new seating strategies without modifying existing code

---

#### **DEMO 4: LSP - Liskov Substitution Principle (Aircraft Hierarchy)**

```
======================================================================
DEMO 4: LSP - Liskov Substitution Principle (Aircraft Hierarchy)
======================================================================

All aircraft types implement the same contract (are fully substitutable):

[OK] Aircraft: Boeing 747
  Seat classes: ['FIRST', 'BUSINESS', 'ECONOMY']
  Luggage allowance: 25.0 kg
  Info: {'aircraft_id': 'B747-01', 'model': 'Boeing 747', ...}

[OK] Aircraft: Boeing 747F
  Seat classes: []
  Luggage allowance: 140000.0 kg
  Info: {'aircraft_id': 'B747F-01', 'model': 'Boeing 747F', ...}

[OK] Both aircraft types satisfy the Aircraft contract!
```

**What This Shows:**
- CommercialAircraft (Boeing 747) and CargoPlanee (Boeing 747F) are both Aircraft
- Both can be used wherever Aircraft type is expected
- They have different implementations but same interface
- You can swap one for the other without breaking code

---

#### **DEMO 5: ISP - Interface Segregation Principle**

```
======================================================================
DEMO 5: ISP - Interface Segregation Principle
======================================================================

[OK] Segregated interfaces for different roles:

  PassengerOperations:
    - search_flights()
    - make_booking()
    - view_my_bookings()
    - cancel_booking()
    - check_booking_status()

  StaffOperations:
    - check_flight_status()
    - get_passenger_list()
    - process_check_in()
    - generate_boarding_pass()
    - handle_cancellation_request()

  AdminOperations:
    - add_flight()
    - add_aircraft()
    - set_pricing_strategy()
    - get_revenue_report()
    - get_system_statistics()

[OK] PaymentProcessor interface (small, focused):
    - process_payment()
    - refund_payment()
    - verify_payment_status()

[OK] Each role has ONLY the methods it needs - no unused interface methods!
```

**What This Shows:**
- Passengers see only passenger-related operations
- Staff see only staff-related operations
- Admins see only admin-related operations
- Each interface is focused and small
- No "fat" interfaces with methods you don't need

---

#### **DEMO 6: DIP - Dependency Inversion Principle**

```
======================================================================
DEMO 6: DIP - Dependency Inversion Principle
======================================================================

[OK] Services depend on abstractions, not concrete implementations:

  FlightService initialized with: InMemoryRepository
  BookingService initialized with:
    - Repository: InMemoryRepository
    - Pricing: DYNAMIC
    - Seating: SEQUENTIAL

  PaymentService can use any payment gateway:
    [OK] STRIPE
    [OK] PAYPAL
    [OK] CREDIT_CARD

  Multiple notification channels:
    [OK] EMAIL
    [OK] SMS
    [OK] PUSH

[OK] Different implementations can be swapped without changing service code!

[OK] Complete booking flow with DIP:
  1. Created booking: BK-3FD2B1C6
  2. Set pricing strategy and calculated: $ 500.00
  3. Processed payment: SUCCESS
  4. Confirmed booking
```

**What This Shows:**
- Services receive implementations via injection
- Can swap StripeGateway with PayPalGateway
- Can swap EmailNotifier with SMSNotifier
- Can swap InMemoryRepository with SQLRepository
- Services don't depend on concrete classes, they depend on interfaces

---

#### **DEMO 7: Complete Flight Booking Flow**

```
======================================================================
DEMO 7: Complete Flight Booking Flow
======================================================================

1. SEARCH FLIGHTS
   Searching: John Smith (Adult) and Tommy Smith (Child)
   Found 1 flight(s)
   Selected: AA101 at $ 250.00

2. RESERVE SEATS
   Reserved 2 seats

3. CREATE BOOKING
   Booking ID: BK-001

4. CALCULATE PRICE
   Total price: $ 500.00

5. PROCESS PAYMENT
   Status: SUCCESS
   Reference: STRIPE-12345

6. CONFIRM AND CHECK-IN
   Status: PAID

7. BOOKING SUMMARY
   booking_id: BK-001
   flight_id: AA101
   passenger_count: 2
   seats: ['10A', '10B']
   status: PAID
   total_price: 500.0
```

**What This Shows:**
- Complete booking workflow from start to finish
- Search → Reserve → Book → Calculate → Pay → Confirm
- Real data flows through the system
- All SOLID principles working together

---

## Part 3: Detailed SOLID Principles Explanation

### 1️⃣ **SRP - Single Responsibility Principle**

**What It Means:**
Each class should have only ONE reason to change.

**Example from the Code:**

```python
# ✓ GOOD - Each class has ONE responsibility

class Flight:
    """Manages only flight data and seats"""
    def reserve_seat(self, count): ...
    def cancel_reservation(self, count): ...
    def get_occupancy_rate(self): ...
    # ONLY flight-related methods

class Passenger:
    """Manages only passenger information"""
    def update_email(self, new_email): ...
    def get_profile(self): ...
    # ONLY passenger-related methods

class Booking:
    """Manages only booking lifecycle"""
    def mark_as_confirmed(self): ...
    def mark_as_paid(self): ...
    # ONLY booking-related methods

# ✗ BAD - Mixing responsibilities
class Flight:
    def reserve_seat(self): ...
    def send_email_to_passenger(self): ...  # NOT Flight's job!
    def process_payment(self): ...          # NOT Flight's job!
```

**Location in Project:**
- `src/core/entities/flight.py`
- `src/core/entities/passenger.py`
- `src/core/entities/booking.py`

**Demo File:**
- `examples/demo_srp.py`
- `run_demo.py srp`

---

### 2️⃣ **OCP - Open/Closed Principle**

**What It Means:**
System should be OPEN for extension but CLOSED for modification.

**Example from the Code:**

```python
# ✓ GOOD - Open for extension, closed for modification

# Base class defines interface
class PricingStrategy(ABC):
    @abstractmethod
    def calculate_price(self, num_passengers, occupancy_rate, days_until_departure):
        pass

# Different implementations (extensions)
class StandardPricing(PricingStrategy):
    def calculate_price(self, ...):
        return base_price * passenger_multiplier

class DynamicPricing(PricingStrategy):
    def calculate_price(self, ...):
        return base_price * occupancy_multiplier * time_multiplier

class SeasonalPricing(PricingStrategy):
    def calculate_price(self, ...):
        return base_price * seasonal_multiplier

class LoyaltyPricing(PricingStrategy):
    def calculate_price(self, ...):
        return base_price * (1 - loyalty_discount)

# Use ANY strategy without modifying existing code
booking_service = BookingService(
    repo,
    pricing_strategy=StandardPricing(100)  # Can swap anytime
)

# Add new strategy without changing anything else
class VIPPricing(PricingStrategy):  # New strategy
    def calculate_price(self, ...):
        return base_price * 0.5  # 50% discount for VIPs
    # Everything still works!

# ✗ BAD - Closed to extension
class BookingService:
    def calculate_price(self, pricing_type):
        if pricing_type == "standard":
            price = base_price
        elif pricing_type == "dynamic":
            price = base_price * occupancy
        elif pricing_type == "seasonal":
            price = base_price * season_multiplier
        # Adding new pricing type requires modifying this function!
```

**Locations in Project:**
- `src/core/services/pricing/` - Pricing strategies
- `src/core/services/seating/` - Seating strategies

**Demo Files:**
- `examples/demo_ocp.py`
- `run_demo.py ocp`

---

### 3️⃣ **LSP - Liskov Substitution Principle**

**What It Means:**
Objects of a subclass should be substitutable for objects of the parent class.

**Example from the Code:**

```python
# ✓ GOOD - Subtypes fully substitutable

class Aircraft(ABC):
    @abstractmethod
    def get_seat_classes(self) -> List[str]: pass
    
    @abstractmethod
    def calculate_luggage_allowance(self) -> float: pass

class CommercialAircraft(Aircraft):
    """Passenger aircraft"""
    def get_seat_classes(self):
        return ["FIRST", "BUSINESS", "ECONOMY"]
    
    def calculate_luggage_allowance(self):
        return 25.0  # kg per passenger

class CargoPlanee(Aircraft):
    """Cargo aircraft"""
    def get_seat_classes(self):
        return []  # No passenger seats
    
    def calculate_luggage_allowance(self):
        return 140000.0  # Total cargo capacity

# Use either aircraft type - they're fully substitutable
def get_aircraft_info(aircraft: Aircraft):
    print(f"Seat classes: {aircraft.get_seat_classes()}")
    print(f"Luggage: {aircraft.calculate_luggage_allowance()} kg")

aircraft_list = [
    CommercialAircraft(...),
    CargoPlanee(...)
]

# This works perfectly with both types!
for aircraft in aircraft_list:
    get_aircraft_info(aircraft)

# ✗ BAD - Violating LSP
class CargoPlanee(Aircraft):
    def get_seat_classes(self):
        raise NotImplementedError("Cargo aircraft don't have seats")
        # This breaks the contract!
```

**Locations in Project:**
- `src/core/entities/aircraft.py`

**Demo Files:**
- `examples/demo_lsp.py`
- `run_demo.py lsp`

---

### 4️⃣ **ISP - Interface Segregation Principle**

**What It Means:**
Clients should not depend on interfaces they don't use. Keep interfaces small and focused.

**Example from the Code:**

```python
# ✓ GOOD - Segregated interfaces

# Passengers only need these operations
class PassengerOperations(ABC):
    @abstractmethod
    def search_flights(self, origin, destination, ...): pass
    
    @abstractmethod
    def make_booking(self, passenger_id, flight_id, ...): pass
    
    @abstractmethod
    def view_my_bookings(self, passenger_id): pass
    
    @abstractmethod
    def cancel_booking(self, booking_id): pass
    
    @abstractmethod
    def check_booking_status(self, booking_id): pass

# Staff only need these operations
class StaffOperations(ABC):
    @abstractmethod
    def check_flight_status(self, flight_id): pass
    
    @abstractmethod
    def get_passenger_list(self, flight_id): pass
    
    @abstractmethod
    def process_check_in(self, booking_id): pass
    
    @abstractmethod
    def generate_boarding_pass(self, booking_id): pass

# Admin only need these operations
class AdminOperations(ABC):
    @abstractmethod
    def add_flight(self, ...): pass
    
    @abstractmethod
    def add_aircraft(self, ...): pass
    
    @abstractmethod
    def set_pricing_strategy(self, ...): pass
    
    @abstractmethod
    def get_revenue_report(self, ...): pass

# Each role implements only what it needs
class PassengerService(PassengerOperations):
    def search_flights(self, ...): ...  # Passenger needs this
    def make_booking(self, ...): ...    # Passenger needs this
    def view_my_bookings(self, ...): ...
    def cancel_booking(self, ...): ...
    def check_booking_status(self, ...): ...

# Passenger doesn't see admin operations!
passenger_service = PassengerService()
passenger_service.search_flights(...)       # ✓ Available
passenger_service.get_revenue_report(...)   # ✗ Not available!

# ✗ BAD - Fat interface (ISP violation)
class UniversalOperations(ABC):
    """Everything for everyone"""
    def search_flights(self, ...): pass
    def add_flight(self, ...): pass
    def process_check_in(self, ...): pass
    def generate_boarding_pass(self, ...): pass
    def get_passenger_list(self, ...): pass
    def process_payment(self, ...): pass
    def verify_payment(self, ...): pass
    def send_email(self, ...): pass
    def send_sms(self, ...): pass
    # ... 50 more methods
    # Passengers must implement methods they don't need!
```

**Locations in Project:**
- `src/core/interfaces/passenger_operations.py`
- `src/core/interfaces/staff_operations.py`
- `src/core/interfaces/admin_operations.py`
- `src/core/interfaces/payment_processor.py`
- `src/core/interfaces/notifier.py`

**Demo Files:**
- `examples/demo_isp.py`
- `run_demo.py isp`

---

### 5️⃣ **DIP - Dependency Inversion Principle**

**What It Means:**
High-level modules should not depend on low-level modules. Both should depend on abstractions.

**Example from the Code:**

```python
# ✓ GOOD - Depends on abstractions (interfaces)

class BookingService:
    def __init__(
        self,
        booking_repository: Repository,      # Abstract interface
        pricing_strategy: PricingStrategy,   # Abstract interface
        seating_strategy: SeatingStrategy,   # Abstract interface
    ):
        self.repository = booking_repository
        self.pricing = pricing_strategy
        self.seating = seating_strategy

# Can inject ANY implementation!
booking_service = BookingService(
    booking_repository=InMemoryRepository(),        # Implementation 1
    pricing_strategy=DynamicPricing(100),          # Implementation 2
    seating_strategy=SequentialAllocation([...])   # Implementation 3
)

# Or swap them anytime
booking_service = BookingService(
    booking_repository=SQLRepository(),            # Different implementation
    pricing_strategy=LoyaltyPricing(100),         # Different implementation
    seating_strategy=WindowPriority([...])        # Different implementation
)

# Payment processing with DIP
payment_service = PaymentService(
    gateway=StripeGateway(...)  # Abstract interface
)

# Later, swap to different gateway
payment_service = PaymentService(
    gateway=PayPalGateway(...)  # Same interface, different implementation
)

# ✗ BAD - Depends on concrete classes (DIP violation)
class BookingService:
    def __init__(self):
        self.repository = InMemoryRepository()      # Hardcoded!
        self.pricing = DynamicPricing(100)         # Hardcoded!
        self.seating = SequentialAllocation([...]) # Hardcoded!
        # Can't swap implementations!
        
# Need to modify BookingService to use different repository
# Need to modify BookingService to use different pricing
# Tightly coupled, hard to test, hard to change
```

**Locations in Project:**
- `src/core/services/booking_service.py`
- `src/core/services/flight_service.py`
- `src/core/services/payment_service.py`
- `src/core/repositories/interfaces.py`
- `src/payment/gateway_interface.py`

**Demo Files:**
- `examples/demo_dip.py`
- `run_demo.py dip`

---

## Part 4: Quick Reference - Running Different Demos

### Run Complete Demo with All SOLID Principles

```bash
python main.py
```

**Shows:**
- All 7 demos in sequence
- SRP → OCP (Pricing) → OCP (Seating) → LSP → ISP → DIP → Complete Flow

---

### Run Individual SOLID Demos

```bash
# SRP Demo - See how each class has single responsibility
python run_demo.py srp
# Output: Flight, Passenger, Booking entities with single responsibilities

# OCP Demo - See how new pricing/seating strategies can be added
python run_demo.py ocp
# Output: Multiple pricing strategies, multiple seating strategies

# LSP Demo - See how aircraft types are substitutable
python run_demo.py lsp
# Output: CommercialAircraft and CargoPlanee used interchangeably

# ISP Demo - See segregated interfaces
python run_demo.py isp
# Output: Different interfaces for different roles

# DIP Demo - See dependency injection
python run_demo.py dip
# Output: Services with swappable dependencies
```

---

### Run All SOLID Demos

```bash
python run_demo.py
```

**Shows:**
- SRP Demo
- OCP Demo
- LSP Demo
- ISP Demo
- DIP Demo

---

### Run Tests

```bash
# Run integration tests (best for seeing how components work together)
pytest tests/test_integration.py -v

# Run all tests
pytest tests/ -v
```

---

## Part 5: Understanding the Code Flow - Step by Step

### When You Run `python main.py`, Here's What Happens:

```
1. Create sample flights
   ↓
2. Create sample passengers
   ↓
3. Demo SRP
   - Create Flight entity (manages only flight data)
   - Create Passenger entity (manages only passenger info)
   - Create Booking entity (manages only booking lifecycle)
   ↓
4. Demo OCP (Pricing)
   - Create StandardPricing instance
   - Create DynamicPricing instance
   - Create SeasonalPricing instance
   - Create LoyaltyPricing instance
   - Calculate prices with each strategy
   ↓
5. Demo OCP (Seating)
   - Create SequentialAllocation instance
   - Create WindowPriority instance
   - Create FamilyAllocation instance
   - Allocate seats with each strategy
   ↓
6. Demo LSP (Aircraft)
   - Create CommercialAircraft instance
   - Create CargoPlanee instance
   - Use both as Aircraft type (substitutable!)
   ↓
7. Demo ISP (Interfaces)
   - Show PassengerOperations interface
   - Show StaffOperations interface
   - Show AdminOperations interface
   - Show PaymentProcessor interface
   - Show Notifier interface
   ↓
8. Demo DIP (Dependency Injection)
   - Create InMemoryRepository
   - Create DynamicPricing instance
   - Create SequentialAllocation instance
   - Inject all into BookingService
   - Inject StripeGateway into PaymentService
   - Create booking, process payment
   ↓
9. Demo Complete Booking Flow
   - Search flights
   - Reserve seats
   - Create booking
   - Calculate price
   - Process payment
   - Confirm booking
   - Display booking summary
   ↓
10. Done! All SOLID principles demonstrated
```

---

## Part 6: File Locations for Each SOLID Principle

### SRP Files (Single Responsibility)

```
src/core/entities/
├── flight.py              ← Flight class (flight responsibility)
├── passenger.py           ← Passenger class (passenger responsibility)
├── booking.py             ← Booking class (booking responsibility)
└── aircraft.py            ← Aircraft class (aircraft responsibility)

examples/demo_srp.py       ← SRP demonstration
```

### OCP Files (Open/Closed Principle)

```
src/core/services/pricing/
├── base_strategy.py       ← Abstract base (interface)
├── standard_pricing.py    ← StandardPricing (implementation)
├── dynamic_pricing.py     ← DynamicPricing (implementation)
├── seasonal_pricing.py    ← SeasonalPricing (implementation)
└── loyalty_pricing.py     ← LoyaltyPricing (implementation)

src/core/services/seating/
├── base_strategy.py       ← Abstract base (interface)
├── sequential_allocation.py ← SequentialAllocation (implementation)
├── window_priority.py     ← WindowPriority (implementation)
└── family_allocation.py   ← FamilyAllocation (implementation)

examples/demo_ocp.py       ← OCP demonstration
```

### LSP Files (Liskov Substitution Principle)

```
src/core/entities/
└── aircraft.py
    ├── Aircraft (abstract base class)
    ├── CommercialAircraft (implementation)
    └── CargoPlanee (implementation)

examples/demo_lsp.py       ← LSP demonstration
```

### ISP Files (Interface Segregation Principle)

```
src/core/interfaces/
├── passenger_operations.py   ← PassengerOperations interface
├── staff_operations.py       ← StaffOperations interface
├── admin_operations.py       ← AdminOperations interface
├── payment_processor.py      ← PaymentProcessor interface
└── notifier.py               ← Notifier interface

examples/demo_isp.py         ← ISP demonstration
```

### DIP Files (Dependency Inversion Principle)

```
src/core/services/
├── booking_service.py    ← BookingService (depends on abstractions)
├── flight_service.py     ← FlightService (depends on abstractions)
└── payment_service.py    ← PaymentService (depends on abstractions)

src/core/repositories/
├── interfaces.py         ← Repository abstract interface
├── in_memory_repo.py     ← InMemoryRepository implementation
└── sql_repo.py           ← SQLRepository implementation

src/payment/
├── gateway_interface.py   ← PaymentProcessor abstract interface
├── stripe_gateway.py      ← StripeGateway implementation
├── paypal_gateway.py      ← PayPalGateway implementation
└── credit_card_gateway.py ← CreditCardGateway implementation

src/core/services/notification/
├── base_notifier.py      ← BaseNotifier abstract interface
├── email_notifier.py     ← EmailNotifier implementation
├── sms_notifier.py       ← SMSNotifier implementation
└── push_notifier.py      ← PushNotifier implementation

examples/demo_dip.py      ← DIP demonstration
```

---

## Part 7: Expected Output Examples

### When You Run `python run_demo.py srp`

```
======================================================================
SRP: Single Responsibility Principle Demo
======================================================================

1. Flight Entity (Responsibility: Flight data & seat management)
----------------------------------------------------------------------
Flight: AA100
Route: New York → Los Angeles
Total seats: 300
Available: 50
Occupancy: 83.3%

Reserving 10 seats...
[OK] Reserved successfully. Available now: 40

2. Passenger Entity (Responsibility: Passenger profile)
----------------------------------------------------------------------
Passenger: John Smith
Email: john.smith@example.com
Phone: +1-212-555-0123
Type: ADULT
Loyalty #: LOY001
Profile: {'id': 'P001', 'name': 'John Smith', ...}

3. Booking Entity (Responsibility: Booking lifecycle)
----------------------------------------------------------------------
Booking ID: BK001
Flight: AA100
Passengers: 1
Seats: ['10A']
Status: PENDING
Total Price: $250.00

Processing booking workflow:
[OK] Confirmed - Status: CONFIRMED
[OK] Payment recorded - Status: CONFIRMED
[OK] Paid - Status: PAID
[OK] Checked in - Status: CHECKED_IN
[OK] Completed - Status: COMPLETED

[OK] SRP Demonstrated: Each entity has ONE clear responsibility!
```

---

## Summary: Quick Start Guide

| Task | Command | What You'll See |
|------|---------|-----------------|
| **See all SOLID demos** | `python main.py` | All 7 demos with explanations |
| **SRP demo only** | `python run_demo.py srp` | Single responsibility in action |
| **OCP demo only** | `python run_demo.py ocp` | Multiple strategies without modification |
| **LSP demo only** | `python run_demo.py lsp` | Aircraft substitutability |
| **ISP demo only** | `python run_demo.py isp` | Segregated interfaces |
| **DIP demo only** | `python run_demo.py dip` | Dependency injection |
| **All SOLID demos** | `python run_demo.py` | All 5 principles in sequence |
| **Run tests** | `pytest tests/ -v` | Verify all components work |
| **Integration tests** | `pytest tests/test_integration.py -v` | Test SOLID principles together |

---

## What Each Principle Solves

| Principle | Problem It Solves | Benefit |
|-----------|-------------------|---------|
| **SRP** | Classes doing too much | Easy to understand, easy to change |
| **OCP** | Adding features requires changing existing code | Add features without touching existing code |
| **LSP** | Subclass doesn't work like parent class | Can safely replace base class with subclass |
| **ISP** | Clients depend on methods they don't use | Clean, focused interfaces |
| **DIP** | High-level code depends on low-level code | Easy to swap implementations, easier testing |

---

This guide provides everything you need to run the project and understand how each SOLID principle is applied!
