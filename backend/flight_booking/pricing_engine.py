# flight_booking/pricing_engine.py

from datetime import datetime
import random

def calculate_dynamic_price(base_price, available_seats, total_seats, departure_datetime, demand_level, seat_no=None):
    # 1. Base Logic (Existing)
    seat_factor = 1 - (available_seats / total_seats)
    
    days_left = (departure_datetime - datetime.now()).days
    if days_left < 0: days_left = 0
    time_factor = 0.02 * max(0, (10 - days_left))

    demand_multiplier = {1: 0.0, 2: 0.10, 3: 0.20}
    demand_factor = demand_multiplier.get(demand_level, 0)
    
    random_factor = random.uniform(0.0, 0.02)

    # Calculate Core Dynamic Price
    price = base_price * (1 + seat_factor + time_factor + demand_factor + random_factor)

    # 2. Seat Position Pricing (NEW)
    seat_surcharge = 0
    if seat_no:
        # Assuming format "12A", "14C", etc.
        letter = seat_no[-1].upper() 
        if letter == 'A':      # Window
            seat_surcharge = 200
        elif letter == 'C':    # Aisle
            seat_surcharge = 100
        # 'B' (Middle) has 0 surcharge

    return round(price + seat_surcharge, 2)