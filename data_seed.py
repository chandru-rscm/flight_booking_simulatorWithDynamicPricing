# flight_booking/data_seed.py
from datetime import datetime, timedelta

from .db import Base, engine, SessionLocal
from .models import Airline, Airport, Flight



def seed():
    # Create tables
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Avoid double seeding
        if db.query(Flight).first():
            print("Database already has data. Skipping seeding.")
            return

        # --- Airlines ---
        ai = Airline(code="AI", name="Air India")
        indigo = Airline(code="6E", name="IndiGo")
        spice = Airline(code="SG", name="SpiceJet")

        db.add_all([ai, indigo, spice])

        # --- Airports ---
        maa = Airport(code="MAA", city="Chennai", name="Chennai International Airport")
        delhi = Airport(code="DEL", city="Delhi", name="Indira Gandhi International Airport")
        bom = Airport(code="BOM", city="Mumbai", name="Chhatrapati Shivaji Maharaj International Airport")
        blr = Airport(code="BLR", city="Bengaluru", name="Kempegowda International Airport")

        db.add_all([maa, delhi, bom, blr])
        db.flush()  # assign IDs for relations

        flights = []
        now = datetime.now()

        # Create flights for next 5 days
        for day in range(1, 6):
            dep_date = now + timedelta(days=day)

            # MAA -> DEL (Air India)
            flights.append(Flight(
                flight_number=f"AI-10{day}",
                airline=ai,
                origin_airport=maa,
                destination_airport=delhi,
                departure_datetime=dep_date.replace(hour=8, minute=0, second=0, microsecond=0),
                arrival_datetime=dep_date.replace(hour=10, minute=30, second=0, microsecond=0),
                base_price=4500 + 100 * day,
                total_seats=180,
                available_seats=180,
                demand_level=1
            ))

            # DEL -> BOM (IndiGo)
            flights.append(Flight(
                flight_number=f"6E-20{day}",
                airline=indigo,
                origin_airport=delhi,
                destination_airport=bom,
                departure_datetime=dep_date.replace(hour=12, minute=0),
                arrival_datetime=dep_date.replace(hour=14, minute=0),
                base_price=3500 + 150 * day,
                total_seats=180,
                available_seats=180,
                demand_level=2
            ))

            # BLR -> MAA (SpiceJet)
            flights.append(Flight(
                flight_number=f"SG-30{day}",
                airline=spice,
                origin_airport=blr,
                destination_airport=maa,
                departure_datetime=dep_date.replace(hour=16, minute=0),
                arrival_datetime=dep_date.replace(hour=18, minute=0),
                base_price=3200 + 120 * day,
                total_seats=160,
                available_seats=160,
                demand_level=3
            ))

        db.add_all(flights)
        db.commit()
        print("Seeding completed successfully.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
