from pydantic import BaseModel
from typing import List, Optional

# --- AUTH ---
class UserSignup(BaseModel):
    email: str
    password: str
    name: str
    phone: str
    dob: str

class UserLogin(BaseModel):
    email: str
    password: str

class VerifyOTP(BaseModel):
    email: str
    otp: str

# --- BOOKING ---
class PassengerDetail(BaseModel):
    first_name: str
    last_name: str
    age: int

class BookingRequest(BaseModel):
    user_email: str
    flight_id: int
    passengers: List[PassengerDetail]
    seat_class: str 
    travel_date: str
    # NEW: Accept specific seat numbers from user
    seat_numbers: List[str]