"""
Core entity classes for Flight Booking System.

SRP: Each entity class has a single, well-defined responsibility.
"""

from .flight import Flight, FlightStatus
from .passenger import Passenger, PassengerType
from .booking import Booking, BookingStatus
from .aircraft import Aircraft, CommercialAircraft, CargoPlanee
from .flight_types import FlightType

__all__ = [
    "Flight",
    "FlightStatus",
    "Passenger",
    "PassengerType",
    "Booking",
    "BookingStatus",
    "Aircraft",
    "CommercialAircraft",
    "CargoPlanee",
    "FlightType",
]
