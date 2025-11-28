# models.py
# Pydantic models for the Flight Booking Simulator

from pydantic import BaseModel
from typing import Optional


class Passenger(BaseModel):
    first_name: str
    last_name: str
    age: int
    phone: int


class BookingRequest(BaseModel):
    flight_id: str
    passenger: Passenger
    travel_date: str
    seat_no: Optional[str] = "Any"


class FlightSchema(BaseModel):
    flight_id: str
    airline_name: str
    origin: str
    destination: str
    arrival_time: str
    departure_time: str
    base_fare: int
    total_seats: int


class FlightOut(BaseModel):
    id: int
    flight_no: str
    origin: str
    destination: str
    departure: str
    arrival: str
    base_fare: float
    total_seats: int
    seats_available: int
    airline_name: str
    duration_minutes: int
