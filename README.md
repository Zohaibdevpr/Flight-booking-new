# Flight Booking System - SOLID Principles Demo

A complete, production-ready Flight Booking System demonstrating all SOLID principles in Python.

## Overview

This project is a comprehensive implementation of a flight booking system that demonstrates all five SOLID principles:

1. **SRP (Single Responsibility Principle)** - Each class has a single, well-defined responsibility
2. **OCP (Open/Closed Principle)** - System is open for extension but closed for modification
3. **LSP (Liskov Substitution Principle)** - Aircraft types are fully substitutable
4. **ISP (Interface Segregation Principle)** - Small, focused interfaces for different roles
5. **DIP (Dependency Inversion Principle)** - High-level modules depend on abstractions

## Project Structure

```
flight-booking-new/
├── src/
│   ├── core/
│   │   ├── entities/              # SRP: Individual entity classes
│   │   │   ├── flight.py
│   │   │   ├── passenger.py
│   │   │   ├── booking.py
│   │   │   ├── aircraft.py        # LSP: Aircraft hierarchy
│   │   │   └── flight_types.py
│   │   │
│   │   ├── interfaces/            # ISP: Segregated interfaces
│   │   │   ├── passenger_operations.py
│   │   │   ├── staff_operations.py
│   │   │   ├── admin_operations.py
│   │   │   ├── payment_processor.py
│   │   │   └── notifier.py
│   │   │
│   │   ├── services/              # DIP: Dependency injection
│   │   │   ├── flight_service.py
│   │   │   ├── booking_service.py
│   │   │   ├── payment_service.py
│   │   │   │
│   │   │   ├── pricing/           # OCP: Pricing strategies
│   │   │   │   ├── base_strategy.py
│   │   │   │   ├── standard_pricing.py
│   │   │   │   ├── dynamic_pricing.py
│   │   │   │   ├── seasonal_pricing.py
│   │   │   │   └── loyalty_pricing.py
│   │   │   │
│   │   │   ├── seating/           # OCP: Seat allocation
│   │   │   │   ├── base_strategy.py
│   │   │   │   ├── sequential_allocation.py
│   │   │   │   ├── window_priority.py
│   │   │   │   └── family_allocation.py
│   │   │   │
│   │   │   └── notification/      # DIP: Notification services
│   │   │       ├── base_notifier.py
│   │   │       ├── email_notifier.py
│   │   │       ├── sms_notifier.py
│   │   │       └── push_notifier.py
│   │   │
│   │   └── repositories/          # DIP: Repository pattern
│   │       ├── interfaces.py
│   │       ├── in_memory_repo.py
│   │       └── sql_repo.py
│   │
│   ├── payment/                   # DIP: Payment abstraction
│   │   ├── gateway_interface.py
│   │   ├── stripe_gateway.py
│   │   ├── paypal_gateway.py
│   │   └── credit_card_gateway.py
│   │
│   └── utils/
│       ├── validators.py
│       └── helpers.py
│
├── examples/                      # SOLID principle demos
│   ├── demo_srp.py
│   ├── demo_ocp.py
│   ├── demo_lsp.py
│   ├── demo_isp.py
│   ├── demo_dip.py
│   └── demo_all_solid.py
│
├── tests/
│   ├── test_basic.py
│   ├── test_integration.py
│   ├── integration/
│   └── unit/
│
├── docs/
│   ├── architecture.md
│   ├── solid_principles.md
│   └── api_reference.md
│
├── main.py                        # Main entry point
├── run_demo.py                    # Quick demo runner
├── requirements.txt
├── setup.py
└── README.md
```

## SOLID Principles Explained

### 1. Single Responsibility Principle (SRP)

Each class has **one reason to change**:

- **Flight** - Manages flight data and seat availability
- **Passenger** - Manages passenger profile information
- **Booking** - Manages booking lifecycle and status
- **Aircraft** - Represents aircraft properties

```python
# Example: Each entity has a single responsibility
flight = Flight(flight_number="AA100", origin="NYC", destination="LAX", ...)
passenger = Passenger(first_name="John", last_name="Doe", ...)
booking = Booking(flight_id="AA100", passenger_ids=["P001"], ...)
```

### 2. Open/Closed Principle (OCP)

System is **open for extension, closed for modification**:

- **Pricing Strategies**: Add new pricing models without modifying existing code
  - StandardPricing
  - DynamicPricing
  - SeasonalPricing
  - LoyaltyPricing

- **Seating Strategies**: Add new seat allocation algorithms
  - SequentialAllocation
  - WindowPriority
  - FamilyAllocation

```python
# Add new pricing strategy without modifying existing code
class MyCustomPricing(PricingStrategy):
    def calculate_price(self, ...):
        # Custom pricing logic
        pass
```

### 3. Liskov Substitution Principle (LSP)

Subtypes must be **fully substitutable** for base types:

- **CommercialAircraft** - Passenger aircraft with cabin classes
- **CargoPlanee** - Cargo aircraft with cargo capacity

Both are substitutable for the base **Aircraft** class:

```python
aircraft_list = [
    CommercialAircraft(...),
    CargoPlanee(...),
]

for aircraft in aircraft_list:
    luggage = aircraft.calculate_luggage_allowance()
    classes = aircraft.get_seat_classes()
```

### 4. Interface Segregation Principle (ISP)

Clients should **not depend on interfaces they don't use**:

- **PassengerOperations** - Only operations passengers need (search, book, view)
- **StaffOperations** - Only operations staff need (check-in, view passengers)
- **AdminOperations** - Only operations admins need (add flights, manage pricing)
- **PaymentProcessor** - Only payment operations
- **Notifier** - Only notification operations

```python
# Passengers only see passenger operations
class PassengerService(PassengerOperations):
    def search_flights(self, ...): pass
    def make_booking(self, ...): pass
    def check_booking_status(self, ...): pass
```

### 5. Dependency Inversion Principle (DIP)

High-level modules should **depend on abstractions**, not concretions:

```python
# DIP: BookingService depends on abstractions
class BookingService:
    def __init__(
        self,
        booking_repository: Repository,              # Abstract
        pricing_strategy: PricingStrategy,          # Abstract
        seating_strategy: SeatingStrategy,          # Abstract
    ):
        self.repository = booking_repository
        self.pricing = pricing_strategy
        self.seating = seating_strategy

# Can use any implementation
booking_service = BookingService(
    booking_repository=InMemoryRepository(),
    pricing_strategy=DynamicPricing(100.0),
    seating_strategy=SequentialAllocation([...]),
)
```

## Features

✅ **Complete Flight Management**
- Create and manage flights
- Track seat availability
- Manage flight status

✅ **Booking System**
- Create bookings with multiple passengers
- Automatic seat allocation
- Booking lifecycle management

✅ **Flexible Pricing**
- Standard flat pricing
- Dynamic pricing based on demand
- Seasonal pricing
- Loyalty-based discounts

✅ **Smart Seat Allocation**
- Sequential allocation
- Window seat priority
- Family seating

✅ **Multi-Channel Notifications**
- Email notifications
- SMS notifications
- Push notifications

✅ **Multiple Payment Gateways**
- Stripe integration
- PayPal integration
- Credit card processing

✅ **Data Persistence**
- In-memory repository
- SQL-based repository (extensible)

## Installation

### Requirements
- Python 3.9+
- No external dependencies (uses only standard library for core functionality)

### Setup

```bash
# Clone the repository
git clone <repository_url>
cd flight-booking-new

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt

# Optional: Install the package
pip install -e .
```

## Usage

### Run Main Booking System

```bash
# Run the main flight booking system
python main.py
```

### Run SOLID Principles Demos

```bash
# Run all demos
python run_demo.py

# Run specific principle demo
python run_demo.py srp     # Single Responsibility Principle
python run_demo.py ocp     # Open/Closed Principle
python run_demo.py lsp     # Liskov Substitution Principle
python run_demo.py isp     # Interface Segregation Principle
python run_demo.py dip     # Dependency Inversion Principle
```

### Run Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_integration.py -v

# Run with coverage
pytest --cov=src
```

## Example Usage

### Creating a Flight Booking

```python
from datetime import datetime, timedelta
from src.core.entities import Flight, Passenger, PassengerType
from src.core.services import BookingService
from src.core.services.pricing import DynamicPricing
from src.core.repositories import InMemoryRepository

# Create repository
repo = InMemoryRepository()

# Create flight
flight = Flight(
    flight_number="AA100",
    origin="New York",
    destination="Los Angeles",
    departure_time=datetime.now() + timedelta(days=5),
    arrival_time=datetime.now() + timedelta(days=5, hours=6),
    aircraft_id="AC001",
    total_seats=300,
    available_seats=100,
    price=250.0,
)
repo.save(flight)

# Create passenger
passenger = Passenger(
    passenger_id="P001",
    first_name="John",
    last_name="Doe",
    email="john@example.com",
    phone="+1-212-555-0123",
    date_of_birth="1990-01-15",
    passenger_type=PassengerType.ADULT,
)

# Create booking service with dependency injection
pricing_strategy = DynamicPricing(base_price=250.0)
booking_service = BookingService(repo, pricing_strategy)

# Create booking
booking = booking_service.create_booking(
    passenger_ids=[passenger.passenger_id],
    flight_id="AA100",
    seat_numbers=["10A"],
)

print(f"Booking created: {booking.booking_id}")
print(f"Status: {booking.status.value}")
print(f"Total price: ${booking.total_price:.2f}")
```

## Testing

The project includes comprehensive tests:

- **Unit Tests**: Individual component tests
- **Integration Tests**: Complete workflow tests
- **SOLID Principle Tests**: Tests demonstrating each SOLID principle

```bash
# Run all tests
pytest tests/ -v

# Run integration tests
pytest tests/test_integration.py -v

# Run with coverage report
pytest --cov=src --cov-report=html
```

## Key Design Patterns Used

1. **Strategy Pattern** - For pricing and seating algorithms
2. **Repository Pattern** - For data access abstraction
3. **Factory Pattern** - For creating domain objects
4. **Dependency Injection** - For loose coupling
5. **Observer Pattern** - For notifications

## Architecture Benefits

✅ **Maintainability** - Each component has a single responsibility
✅ **Extensibility** - Add new features without modifying existing code
✅ **Testability** - Components are loosely coupled and easy to unit test
✅ **Flexibility** - Swap implementations with dependency injection
✅ **Scalability** - Can be extended to support more features

## Learning Resources

This project demonstrates:

- How to apply SOLID principles in a real-world application
- How to structure large Python projects
- How to implement design patterns correctly
- How to write testable, maintainable code
- How to use type hints effectively

Each SOLID principle has a dedicated demo file in the `examples/` directory showing practical applications.

## Contributing

Contributions are welcome! When adding new features:

1. Follow SOLID principles
2. Add comprehensive tests
3. Update documentation
4. Use type hints
5. Run tests before submitting

## License

This project is provided as an educational example.

## Author

Created as a comprehensive example of SOLID principles in Python.

---

For more details, see the documentation in the `docs/` directory.
