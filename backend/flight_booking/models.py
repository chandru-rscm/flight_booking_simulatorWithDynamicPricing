from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from db import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    
    # --- NEW DETAILS ---
    name = Column(String)
    phone = Column(String)
    dob = Column(String)
    # -------------------

    otp = Column(String, nullable=True)

class Airline(Base):
    __tablename__ = "airlines"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    name = Column(String)
    flights = relationship("Flight", back_populates="airline")

class Airport(Base):
    __tablename__ = "airports"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    city = Column(String)
    name = Column(String)
    origin_flights = relationship("Flight", back_populates="origin_airport", foreign_keys="Flight.origin_id")
    destination_flights = relationship("Flight", back_populates="destination_airport", foreign_keys="Flight.destination_id")

class Flight(Base):
    __tablename__ = "flights"
    id = Column(Integer, primary_key=True, index=True)
    flight_number = Column(String, unique=True, index=True)
    airline_id = Column(Integer, ForeignKey("airlines.id"))
    origin_id = Column(Integer, ForeignKey("airports.id"))
    destination_id = Column(Integer, ForeignKey("airports.id"))
    departure_datetime = Column(DateTime)
    arrival_datetime = Column(DateTime)
    base_price = Column(Float)
    total_seats = Column(Integer)
    available_seats = Column(Integer)
    demand_level = Column(Integer, default=1) 
    airline = relationship("Airline", back_populates="flights")
    origin_airport = relationship("Airport", foreign_keys=[origin_id], back_populates="origin_flights")
    destination_airport = relationship("Airport", foreign_keys=[destination_id], back_populates="destination_flights")

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String) 
    pnr = Column(String, unique=True, index=True, nullable=True)
    flight_id = Column(Integer, ForeignKey("flights.id"))
    passenger_names = Column(String) 
    passenger_count = Column(Integer)
    seat_numbers = Column(String)
    travel_date = Column(String)
    total_price = Column(Float)
    status = Column(String, default="PENDING") 
    created_at = Column(DateTime, default=datetime.utcnow)