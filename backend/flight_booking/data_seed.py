from sqlalchemy.orm import Session
from .db import SessionLocal, engine
from .models import Airline, Airport, Flight, Base
from datetime import datetime, timedelta
import random

Base.metadata.create_all(bind=engine)

def seed_data():
    db: Session = SessionLocal()

    # ============================
    # 1. Seed Airlines
    # ============================
    airlines = [
        Airline(code="AI", name="Air India"),
        Airline(code="6E", name="IndiGo"),
        Airline(code="SG", name="SpiceJet"),
    ]

    for a in airlines:
        existing = db.query(Airline).filter(Airline.code == a.code).first()
        if not existing:
            db.add(a)

    # ============================
    # 2. Seed Airports
    # ============================
    airports = [
        Airport(code="MAA", city="Chennai", name="Chennai International Airport"),
        Airport(code="DEL", city="Delhi", name="Indira Gandhi International Airport"),
        Airport(code="BOM", city="Mumbai", name="Chhatrapati Shivaji Airport"),
    ]

    for ap in airports:
        existing = db.query(Airport).filter(Airport.code == ap.code).first()
        if not existing:
            db.add(ap)

    db.commit()

    # Refresh IDs
    airlines = db.query(Airline).all()
    airports = db.query(Airport).all()

    # Airport lookup helper
    airport_dict = {a.code: a.id for a in airports}

    # ============================
    # 3. Seed Flights
    # ============================
    flight_list = [
        ("AI101", "AI", "MAA", "DEL"),
        ("AI202", "AI", "DEL", "BOM"),
        ("6E303", "6E", "BOM", "DEL"),
        ("6E404", "6E", "DEL", "MAA"),
        ("SG505", "SG", "MAA", "BOM"),
    ]

    for f_no, airline_code, origin, dest in flight_list:
        airline = db.query(Airline).filter(Airline.code == airline_code).first()

        exists = db.query(Flight).filter(Flight.flight_number == f_no).first()
        if exists:
            continue

        departure = datetime.now() + timedelta(days=random.randint(1, 10))
        arrival = departure + timedelta(hours=2)

        flight = Flight(
            flight_number=f_no,
            airline_id=airline.id,
            origin_airport_id=airport_dict[origin],
            destination_airport_id=airport_dict[dest],
            departure_datetime=departure,
            arrival_datetime=arrival,
            base_price=random.randint(3000, 9000),
            total_seats=120,
            available_seats=120,
            demand_level=random.randint(1, 3)
        )
        db.add(flight)

    db.commit()
    db.close()

    print("Database seeded successfully!")


if __name__ == "__main__":
    seed_data()
