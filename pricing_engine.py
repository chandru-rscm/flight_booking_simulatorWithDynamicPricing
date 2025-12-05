# flight_booking/pricing_engine.py
from datetime import datetime


def calculate_dynamic_price(
    base_price: float,
    total_seats: int,
    available_seats: int,
    departure_datetime,
    demand_level: int
) -> float:
    """
    Dynamic pricing logic:
    - Remaining seat percentage
    - Time to departure
    - Demand level (1=low, 2=medium, 3=high)
    """

    price = base_price

    # --- Seat availability factor ---
    if total_seats > 0:
        remaining_percent = available_seats / total_seats
    else:
        remaining_percent = 0

    # If < 20% seats left → +20%
    if remaining_percent < 0.2:
        price *= 1.20
    # Else if < 50% seats left → +10%
    elif remaining_percent < 0.5:
        price *= 1.10

    # --- Time to departure factor ---
    now = datetime.now()
    diff = departure_datetime - now
    days_to_departure = diff.days

    # If flight is within 1 day → +25%
    if days_to_departure <= 1:
        price *= 1.25
    # If within 3 days → +15%
    elif days_to_departure <= 3:
        price *= 1.15
    # If within 7 days → +5%
    elif days_to_departure <= 7:
        price *= 1.05

    # --- Demand level factor ---
    # demand_level: 1 = low, 2 = medium, 3 = high
    if demand_level == 2:
        price *= 1.10   # +10%
    elif demand_level == 3:
        price *= 1.25   # +25%

    # Round to nearest paisa
    return round(price, 2)
