# pricing.py
from datetime import datetime

# This value will be updated from demand_simulator.py
from demand_simulator import DEMAND_LEVEL


def calculate_dynamic_price(
    base_price: float,
    seats_available: int,
    seats_total: int,
    departure_date: str,
) -> float:
    """
    Dynamic pricing formula based on:
    - remaining seats
    - time left for departure
    - global demand level
    - fare tiers
    """

    # 1. Remaining seat percentage
    remaining_pct = seats_available / seats_total

    if remaining_pct > 0.8:
        seat_factor = 0.95
    elif remaining_pct > 0.4:
        seat_factor = 1.0
    elif remaining_pct > 0.1:
        seat_factor = 1.15
    else:
        seat_factor = 1.30

    # 2. Time until departure
    today = datetime.now().date()
    dep = datetime.strptime(departure_date, "%Y-%m-%d").date()
    days_left = (dep - today).days

    if days_left > 30:
        time_factor = 0.90
    elif days_left >= 7:
        time_factor = 1.0
    elif days_left >= 1:
        time_factor = 1.10
    else:
        time_factor = 1.25

    # 3. Demand level (updated every 30 sec)
    demand_factor = DEMAND_LEVEL

    # 4. Base fare tiering
    if base_price < 4000:
        tier_factor = 1.0
    elif base_price <= 7000:
        tier_factor = 1.10
    else:
        tier_factor = 1.20

    final_price = base_price * seat_factor * time_factor * demand_factor * tier_factor

    return round(final_price, 2)
