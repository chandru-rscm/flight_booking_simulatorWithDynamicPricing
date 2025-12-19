from datetime import datetime
import random

def calculate_dynamic_price(base_price, available_seats, total_seats, departure_datetime, demand_level):
    # Seat availability factor
    seat_factor = 1 - (available_seats / total_seats)

    # Time factor
    days_left = (departure_datetime - datetime.now()).days
    if days_left < 0:
        days_left = 0

    time_factor = 0.02 * max(0, (10 - days_left))  # increase price when trip is soon

    # Demand factor
    demand_multiplier = {1: 0.0, 2: 0.10, 3: 0.20}
    demand_factor = demand_multiplier.get(demand_level, 0)

    # Random variation
    random_factor = random.uniform(0.0, 0.05)

    dynamic_price = base_price * (1 + seat_factor + time_factor + demand_factor + random_factor)

    return round(dynamic_price, 2)
