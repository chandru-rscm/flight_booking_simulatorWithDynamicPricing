# data_seed.py
"""
Simulated external airline API data feed.
Used by:
    POST /external/sync
This provides mock flight schedules that get inserted into the database
ONLY if the same flight_no + departure_date does not already exist.
"""

def get_external_airline_data():
    """
    Returns a list of external flights in dict format.
    These mimic real external airline schedule APIs.
    """
    return [
        {
            "flight_no": "AI-550",
            "origin": "DEL",
            "destination": "MAA",
            "departure_date": "2025-12-02",
            "departure_time": "06:00",
            "arrival_time": "08:45",
            "duration_minutes": 165,
            "base_price": 6200.0,
            "seats_total": 180,
            "seats_available": 100,
            "airline": "Air India"
        },
        {
            "flight_no": "6E-777",
            "origin": "BLR",
            "destination": "DEL",
            "departure_date": "2025-12-02",
            "departure_time": "09:30",
            "arrival_time": "12:10",
            "duration_minutes": 160,
            "base_price": 5400.0,
            "seats_total": 180,
            "seats_available": 120,
            "airline": "IndiGo"
        },
        {
            "flight_no": "SG-909",
            "origin": "MUM",
            "destination": "COK",
            "departure_date": "2025-12-03",
            "departure_time": "14:20",
            "arrival_time": "16:10",
            "duration_minutes": 110,
            "base_price": 4800.0,
            "seats_total": 160,
            "seats_available": 90,
            "airline": "SpiceJet"
        },
        {
            "flight_no": "UK-888",
            "origin": "DEL",
            "destination": "GOI",
            "departure_date": "2025-12-04",
            "departure_time": "07:40",
            "arrival_time": "10:00",
            "duration_minutes": 140,
            "base_price": 5900.0,
            "seats_total": 170,
            "seats_available": 140,
            "airline": "Vistara"
        }
    ]
