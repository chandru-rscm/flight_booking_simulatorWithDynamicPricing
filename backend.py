# backend.py
# Flight Booking Simulator – Milestone 1: Core Flight Search & Data Management

from fastapi import FastAPI, HTTPException, status, Query
from typing import Optional, List
from datetime import datetime, timedelta
import random

# Import Pydantic models
from models import Passenger, BookingRequest, FlightSchema, FlightOut

# Import DB utilities
from data_seed import get_db_connection, init_db_if_needed


app = FastAPI(title="Flight Booking Simulator - Milestone 1")


@app.on_event("startup")
def on_startup():
    init_db_if_needed()


@app.get("/home")
def read_root():
    return {"message": "Welcome to the flight booking system"}


@app.post("/bookings/create", status_code=status.HTTP_201_CREATED)
def create_booking_with_status(booking: BookingRequest):
    try:
        datetime.strptime(booking.travel_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid travel_date format. Use YYYY-MM-DD.",
        )
    return {
        "message": "Booking created",
        "booking_id": 5876,
        "request_data": booking,
    }


@app.get("/sample/passenger")
def get_passenger_sample():
    return {"first_name": "John", "last_name": "Doe", "age": 30, "phone": 123456789}


@app.get("/sample/bookings")
def get_booking_sample():
    return {
        "flight_id": "AI1",
        "passenger": {
            "first_name": "John",
            "last_name": "Doe",
            "age": 30,
            "phone": 123456789,
        },
        "travel_date": "2025-10-10",
        "seat_no": "20",
    }


@app.get("/airline_names")
def get_all_airlines():
    return [
        {"flight_id": "AI1", "name": "Air India"},
        {"flight_id": "6E", "name": "IndiGo"},
        {"flight_id": "SG", "name": "SpiceJet"},
    ]


@app.get("/health")
def health_check():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM flights;")
    total_flights = cur.fetchone()[0]
    conn.close()
    return {"status": "healthy", "total_flights": total_flights}


@app.get("/flights", response_model=dict)
def list_flights(
    origin: Optional[str] = Query(None),
    destination: Optional[str] = Query(None),
    date: Optional[str] = Query(None),
    sort_by: str = Query("price", pattern="^(price|duration)$"),
    order: str = Query("asc", pattern="^(asc|desc)$"),
):
    conn = get_db_connection()
    cur = conn.cursor()

    query = "SELECT * FROM flights WHERE 1=1"
    params = []

    if origin:
        query += " AND lower(origin)=lower(?)"
        params.append(origin)

    if destination:
        query += " AND lower(destination)=lower(?)"
        params.append(destination)

    if date:
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except:
            raise HTTPException(400, "Invalid date format. Use YYYY-MM-DD.")
        query += " AND date(departure)=date(?)"
        params.append(date)

    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()

    flights: List[FlightOut] = []

    for row in rows:
        dep = datetime.fromisoformat(row["departure"])
        arr = datetime.fromisoformat(row["arrival"])
        duration = int((arr - dep).total_seconds() // 60)

        flights.append(
            FlightOut(
                id=row["id"],
                flight_no=row["flight_no"],
                origin=row["origin"],
                destination=row["destination"],
                departure=row["departure"],
                arrival=row["arrival"],
                base_fare=row["base_fare"],
                total_seats=row["total_seats"],
                seats_available=row["seats_available"],
                airline_name=row["airline_name"],
                duration_minutes=duration,
            )
        )

    reverse = order == "desc"
    if sort_by == "price":
        flights.sort(key=lambda f: f.base_fare, reverse=reverse)
    else:
        flights.sort(key=lambda f: f.duration_minutes, reverse=reverse)

    return {"total_results": len(flights), "sort_by": sort_by, "order": order, "results": flights}


@app.get("/flights/{flight_no}", response_model=FlightOut)
def get_flight_info(flight_no: str):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM flights WHERE flight_no=?", (flight_no,))
    row = cur.fetchone()
    conn.close()

    if not row:
        raise HTTPException(404, f"Flight {flight_no} not found")

    dep = datetime.fromisoformat(row["departure"])
    arr = datetime.fromisoformat(row["arrival"])
    duration = int((arr - dep).total_seconds() // 60)

    return FlightOut(
        id=row["id"],
        flight_no=row["flight_no"],
        origin=row["origin"],
        destination=row["destination"],
        departure=row["departure"],
        arrival=row["arrival"],
        base_fare=row["base_fare"],
        total_seats=row["total_seats"],
        seats_available=row["seats_available"],
        airline_name=row["airline_name"],
        duration_minutes=duration,
    )


@app.get("/external/airline_feed")
def simulate_external_airline_feed(origin: str, destination: str, date: str):
    try:
        travel_date = datetime.strptime(date, "%Y-%m-%d")
    except:
        raise HTTPException(400, "Invalid date format. Use YYYY-MM-DD.")

    airlines = ["Air India", "IndiGo", "SpiceJet", "Vistara"]
    results = []

    for i in range(3):
        dep = travel_date + timedelta(hours=8 + i * 3)
        arr = dep + timedelta(hours=2)
        base = random.choice([5500, 6000, 6500, 7000])

        results.append(
            {
                "flight_no": f"EXT{i+1}",
                "airline_name": random.choice(airlines),
                "origin": origin,
                "destination": destination,
                "departure": dep.strftime("%Y-%m-%d %H:%M:%S"),
                "arrival": arr.strftime("%Y-%m-%d %H:%M:%S"),
                "base_fare": base,
                "dynamic_price": base + random.randint(-500, 1500),
                "seats_available": random.randint(20, 180),
                "source": "Simulated external API",
            }
        )

    return {
        "origin": origin,
        "destination": destination,
        "date": date,
        "external_flights": results,
    }
