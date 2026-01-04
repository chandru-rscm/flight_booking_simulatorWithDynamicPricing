import re

def calculate_dynamic_price(base_price, available_seats, total_seats, departure_date, demand_level, seat_no=None):
    # 1. Start with Base Price
    price = base_price
    
    # 2. Demand Factor
    # If demand is High (3) -> +50%, Low (1) -> -10%
    if demand_level == 3:
        price *= 1.5
    elif demand_level == 1:
        price *= 0.9

    # 3. Scarcity Factor (If plane is >80% full)
    if total_seats > 0:
        occupancy = (total_seats - available_seats) / total_seats
        if occupancy > 0.8:
            price *= 1.2

    # 4. Business Class Logic (The new part!)
    if seat_no:
        # Extract row number (e.g., "2A" -> 2)
        match = re.match(r"(\d+)", str(seat_no))
        if match:
            row = int(match.group(1))
            # Rows 1-4 are Business Class -> 2.5x Price
            if row < 5:
                price *= 2.5

    return round(price, 2)