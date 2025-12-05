# flight_booking/backend.py
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, aliased

from .db import get_db
from .models import Flight, Airport
from .pricing_engine import calculate_dynamic_price


app = FastAPI(title="Flight Booking Simulator with Dynamic Pricing")


@app.get("/flights")
def get_all_flights(db: Session = Depends(get_db)):
    """
    Return all flights with base and dynamic price.
    (Nice for demo: you can show how price changes over time.)
    """
    flights = db.query(Flight).all()
    result = []

    for f in flights:
        dynamic_price = calculate_dynamic_price(
            base_price=f.base_price,
            total_seats=f.total_seats,
            available_seats=f.available_seats,
            departure_datetime=f.departure_datetime,
            demand_level=f.demand_level or 1
        )

        result.append({
            "flight_id": f.id,
            "flight_number": f.flight_number,
            "airline": f.airline.name if f.airline else None,
            "airline_code": f.airline.code if f.airline else None,
            "origin": f.origin_airport.code if f.origin_airport else None,
            "origin_city": f.origin_airport.city if f.origin_airport else None,
            "destination": f.destination_airport.code if f.destination_airport else None,
            "destination_city": f.destination_airport.city if f.destination_airport else None,
            "departure_time": f.departure_datetime,
            "arrival_time": f.arrival_datetime,
            "base_price": f.base_price,
            "dynamic_price": dynamic_price,
            "total_seats": f.total_seats,
            "available_seats": f.available_seats,
            "demand_level": f.demand_level,
        })

    return result


@app.get("/search")
def search_flights(
    origin: str,
    destination: str,
    date_str: str,
    sort_by: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    Search flights by origin, destination and date.
    Uses dynamic pricing. Optional sort_by: 'price' or 'duration'.
    """
    origin = origin.upper()
    destination = destination.upper()

    # --- Validation ---
    if len(origin) != 3 or len(destination) != 3:
        raise HTTPException(
            status_code=400,
            detail="Origin and destination must be 3-letter airport codes (e.g., MAA, DEL)."
        )

    if origin == destination:
        raise HTTPException(
            status_code=400,
            detail="Origin and destination cannot be the same."
        )

    try:
        journey_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid date format. Use YYYY-MM-DD."
        )

 
    OriginAirport = aliased(Airport)
    DestinationAirport = aliased(Airport)

    query = (
        db.query(Flight)
        .join(OriginAirport, Flight.origin_airport_id == OriginAirport.id)
        .join(DestinationAirport, Flight.destination_airport_id == DestinationAirport.id)
        .filter(OriginAirport.code == origin)
        .filter(DestinationAirport.code == destination)
    )

    flights = query.all()


    flights = [
        f for f in flights
        if f.departure_datetime.date() == journey_date
    ]

    if not flights:
        return []  


    result = []
    for f in flights:
        duration_minutes = int(
            (f.arrival_datetime - f.departure_datetime).total_seconds() // 60
        )

        dynamic_price = calculate_dynamic_price(
            base_price=f.base_price,
            total_seats=f.total_seats,
            available_seats=f.available_seats,
            departure_datetime=f.departure_datetime,
            demand_level=f.demand_level or 1
        )

        result.append({
            "flight_id": f.id,
            "flight_number": f.flight_number,
            "airline": f.airline.name if f.airline else None,
            "airline_code": f.airline.code if f.airline else None,
            "origin": f.origin_airport.code if f.origin_airport else None,
            "destination": f.destination_airport.code if f.destination_airport else None,
            "departure_time": f.departure_datetime,
            "arrival_time": f.arrival_datetime,
            "duration_minutes": duration_minutes,
            "base_price": f.base_price,
            "dynamic_price": dynamic_price,
            "available_seats": f.available_seats,
            "demand_level": f.demand_level,
        })

    
    if sort_by:
        if sort_by == "price":
            result.sort(key=lambda x: x["dynamic_price"])
        elif sort_by == "duration":
            result.sort(key=lambda x: x["duration_minutes"])
        else:
            raise HTTPException(
                status_code=400,
                detail="Invalid sort_by. Use 'price' or 'duration'."
            )

    return result


@app.get("/external/airline-feed")
def simulated_external_airline_feed():
    """
    Simulated external airline schedule API.
    You can mention this as 'mock integration with external airline systems'.
    """
    return {
        "provider": "MockExternalAirlineAPI",
        "flights": [
            {
                "flight_number": "EXT-901",
                "origin": "BLR",
                "destination": "BOM",
                "departure_time": "2025-12-10T10:00:00",
                "arrival_time": "2025-12-10T11:30:00",
                "base_price": 3200,
            },
            {
                "flight_number": "EXT-902",
                "origin": "MAA",
                "destination": "DEL",
                "departure_time": "2025-12-11T09:00:00",
                "arrival_time": "2025-12-11T11:30:00",
                "base_price": 4100,
            },
        ],
    }
