# models.py
from pydantic import BaseModel, Field
from typing import Optional, List


class Flight(BaseModel):
    id: int
    flight_no: str
    origin: str
    destination: str
    departure_date: str
    departure_time: str
    arrival_time: str
    duration_minutes: int
    base_price: float
    seats_total: int
    seats_available: int
    airline: str

    # From Module 2 – dynamic pricing
    dynamic_price: Optional[float] = None


class FlightSearchQuery(BaseModel):
    origin: str = Field(..., min_length=3, max_length=3)
    destination: str = Field(..., min_length=3, max_length=3)
    departure_date: str = Field(
        ...,
        pattern=r"^\d{4}-\d{2}-\d{2}$",
    )


class FlightSearchFilters(BaseModel):
    sort_by: Optional[str] = Field(
        default=None,
        description="Optional sorting key: 'price' or 'duration'"
    )


# -----------------------------
# Booking models (Module 3)
# -----------------------------

class BookingCreate(BaseModel):
    """
    Request body for creating a new booking.
    This is equivalent to a Django Form/Serializer for booking input.
    """
    flight_id: int
    passenger_name: str
    passenger_email: str
    passenger_phone: str
    seat_number: Optional[str] = None


class Booking(BaseModel):
    """
    Response model representing a booking stored in the database.
    """
    id: int
    pnr: str
    flight_id: int
    passenger_name: str
    passenger_email: str
    passenger_phone: str
    seat_number: Optional[str]
    status: str
    price_paid: float
    booked_at: str
