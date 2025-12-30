from db import SessionLocal
from models import Flight
import random
import time

def simulate_demand():
    while True:
        db = SessionLocal()
        flights = db.query(Flight).all()

        for f in flights:
            # Randomly adjust demand level (1 to 3)
            f.demand_level = random.randint(1, 3)

            # Simulate seats filling
            if f.available_seats > 0 and random.random() < 0.3:
                f.available_seats -= 1  

        db.commit()
        db.close()

        print("Demand simulation updated.")
        time.sleep(15)  # every 15 sec
