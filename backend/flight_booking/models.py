from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db import Base
from datetime import datetime


class Airline(Base):
    __tablename__ = "airlines"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    name = Column(String)

    # Relationship to Flight
    flights = relationship("Flight", back_populates="airline")


class Airport(Base):
    __tablename__ = "airports"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    city = Column(String)
    name = Column(String)

    # Relationships to Flight (Fixed Foreign Keys)
    origin_flights = relationship(
        "Flight",
        back_populates="origin_airport",
        foreign_keys="Flight.origin_id"  # Fixed: matches the column name in Flight
    )
    destination_flights = relationship(
        "Flight",
        back_populates="destination_airport",
        foreign_keys="Flight.destination_id" # Fixed: matches the column name in Flight
    )


class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True)
    flight_number = Column(String, unique=True, index=True)
    
    # Foreign Keys
    airline_id = Column(Integer, ForeignKey("airlines.id")) # Added missing FK
    origin_id = Column(Integer, ForeignKey("airports.id"))
    destination_id = Column(Integer, ForeignKey("airports.id"))
    
    departure_datetime = Column(DateTime)
    arrival_datetime = Column(DateTime)
    base_price = Column(Float)
    total_seats = Column(Integer)
    available_seats = Column(Integer)
    demand_level = Column(Integer, default=1) 

    # Relationships
    airline = relationship("Airline", back_populates="flights")
    
    origin_airport = relationship(
        "Airport", 
        foreign_keys=[origin_id], 
        back_populates="origin_flights"
    )
    destination_airport = relationship(
        "Airport", 
        foreign_keys=[destination_id], 
        back_populates="destination_flights"
    )


class Booking(Base):
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    pnr = Column(String, unique=True, index=True)
    flight_id = Column(Integer, ForeignKey("flights.id"))
    passenger_name = Column(String)
    seat_no = Column(String)
    
    # --- NEW COLUMN ---
    travel_date = Column(String)  # Stores date as "YYYY-MM-DD"
    # ------------------

    price = Column(Float)
    status = Column(String, default="PENDING") 
    created_at = Column(DateTime, default=datetime.utcnow)