# flight_booking/schemas.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# -----------------------------
# Request Models
# -----------------------------

class Passenger(BaseModel):
    first_name: str
    last_name: str
    age: int
    phone: int


class BookingRequest(BaseModel):
    flight_id: int
    passenger: Passenger
    seat_no: str
    travel_date: str


# -----------------------------
# Response Models
# -----------------------------

class FlightResponse(BaseModel):
    flight_id: int
    flight_number: str
    origin: str
    destination: str
    departure: datetime
    arrival: datetime
    dynamic_price: float
    available_seats: int

    class Config:
        orm_mode = True


class BookingResponse(BaseModel):
    pnr: str
    passenger_name: str
    flight_id: int
    seat_no: str
    price: float
    status: str
    created_at: datetime

    class Config:
        orm_mode = True
