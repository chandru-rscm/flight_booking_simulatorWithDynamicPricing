from sqlalchemy.orm import Session
from db import SessionLocal, engine
from models import Base, Airline, Airport, Flight
from datetime import datetime, timedelta
import random

def seed_data():
    db = SessionLocal()
    
    if db.query(Airline).first():
        db.close()
        print("✅ Data already exists. Skipping seed.")
        return

    print("🌱 Seeding data with MULTIPLE FLIGHTS per day...")

    airlines = [
        Airline(code="6E", name="IndiGo"),
        Airline(code="AI", name="Air India"),
        Airline(code="UK", name="Vistara"),
        Airline(code="SG", name="SpiceJet"),
        Airline(code="QP", name="Akasa Air"),
    ]
    db.add_all(airlines)
    db.commit()

    airports = [
        Airport(code="DEL", city="Delhi", name="Indira Gandhi International Airport"),
        Airport(code="BOM", city="Mumbai", name="Chhatrapati Shivaji Maharaj International Airport"),
        Airport(code="BLR", city="Bangalore", name="Kempegowda International Airport"),
        Airport(code="MAA", city="Chennai", name="Chennai International Airport"),
        Airport(code="HYD", city="Hyderabad", name="Rajiv Gandhi International Airport"),
        Airport(code="TRZ", city="Trichy", name="Tiruchirappalli International Airport"),
        Airport(code="CCU", city="Kolkata", name="Netaji Subhas Chandra Bose Airport"),
    ]
    db.add_all(airports)
    db.commit()

    all_airlines = db.query(Airline).all()
    all_airports = db.query(Airport).all()

    flights = []
    flight_counter = 101
    
    today = datetime.now()
    
    for origin in all_airports:
        for destination in all_airports:
            if origin.id == destination.id:
                continue 

            for day_offset in range(0, 16): 
                
                # RANDOM LOGIC: 
                # Randomly decide if there are 0, 1, 2, 3, or 4 flights today
                num_flights_today = random.randint(0, 4)

                for _ in range(num_flights_today):
                    airline = random.choice(all_airlines)
                    
                    # Random time logic to ensure variety
                    hour = random.choice([5, 7, 9, 11, 14, 16, 18, 20, 22])
                    minute = random.choice([0, 15, 30, 45])
                    
                    hour = min(23, hour + random.randint(0, 1))

                    flight_date = today + timedelta(days=day_offset)
                    dep_time = flight_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
                    
                    duration = random.randint(60, 180)
                    arr_time = dep_time + timedelta(minutes=duration)

                    f_no = f"{airline.code}{flight_counter}"
                    flight_counter += 1
                    
                    base_price = random.randint(3500, 12000)

                    flight = Flight(
                        flight_number=f_no,
                        airline_id=airline.id,
                        origin_id=origin.id,
                        destination_id=destination.id,
                        departure_datetime=dep_time,
                        arrival_datetime=arr_time,
                        base_price=base_price,
                        total_seats=180,
                        available_seats=random.randint(120, 180),
                        demand_level=random.randint(1, 3)
                    )
                    flights.append(flight)

    db.add_all(flights)
    db.commit()
    db.close()
    
    print(f"✅ Data seeded successfully! ({len(flights)} Flights Created)")

if __name__ == "__main__":
    seed_data()