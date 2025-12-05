# flight_booking/demand_simulator.py
import random
import time
from datetime import datetime

from .db import SessionLocal
from .models import Flight



def simulate_demand_once():
    db = SessionLocal()
    try:
        flights = db.query(Flight).all()
        for f in flights:
            if f.available_seats > 0:
                reduction = random.randint(0, 3)  
                f.available_seats = max(0, f.available_seats - reduction)

            f.demand_level = random.choice([1, 2, 3])

            print(
                f"[{datetime.now()}] Flight {f.flight_number}: "
                f"seats={f.available_seats}, demand={f.demand_level}"
            )

        db.commit()
    finally:
        db.close()


def run_simulator_loop():
    while True:
        simulate_demand_once()
        time.sleep(60)  


if __name__ == "__main__":
    run_simulator_loop()
