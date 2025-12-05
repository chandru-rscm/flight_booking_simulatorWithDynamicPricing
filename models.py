# flight_booking/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base   



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

    origin_flights = relationship(
        "Flight",
        back_populates="origin_airport",
        foreign_keys="Flight.origin_airport_id"
    )
    destination_flights = relationship(
        "Flight",
        back_populates="destination_airport",
        foreign_keys="Flight.destination_airport_id"
    )


class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True)
    flight_number = Column(String, index=True)       

    airline_id = Column(Integer, ForeignKey("airlines.id"))
    origin_airport_id = Column(Integer, ForeignKey("airports.id"))
    destination_airport_id = Column(Integer, ForeignKey("airports.id"))

    departure_datetime = Column(DateTime)
    arrival_datetime = Column(DateTime)

    base_price = Column(Float)
    total_seats = Column(Integer)
    available_seats = Column(Integer)

   
    # 1 = low, 2 = medium, 3 = high
    demand_level = Column(Integer, default=1)

    airline = relationship("Airline", back_populates="flights")
    origin_airport = relationship(
        "Airport",
        foreign_keys=[origin_airport_id],
        back_populates="origin_flights"
    )
    destination_airport = relationship(
        "Airport",
        foreign_keys=[destination_airport_id],
        back_populates="destination_flights"
    )
