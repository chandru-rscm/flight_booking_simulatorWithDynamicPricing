# backend.py
"""
Flight Booking Simulator Backend
Combines:
- Module 1: Core Flight Search & Data Management
- Module 2: Dynamic Pricing Engine
- Module 3: Booking Workflow & Transaction Management
"""

from fastapi import FastAPI, HTTPException, Query, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from typing import List, Optional
from datetime import datetime
import random
import sqlite3

from db import init_db, get_connection
from models import Flight, Booking, BookingCreate
from data_seed import get_external_airline_data
from pricing import calculate_dynamic_price
from demand_simulator import start_demand_simulator


# ---------------------------------------------------------
# App setup
# ---------------------------------------------------------

app = FastAPI(
    title="Flight Booking Simulator",
    description=(
        "Backend for Flight Booking System:\n"
        "- Core search & data management\n"
        "- Dynamic pricing engine\n"
        "- Booking workflow & transaction management"
    ),
    version="1.0.0"
)
# Serve CSS + JS from /static
# Serve static files (CSS/JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve frontend pages
@app.get("/", response_class=HTMLResponse)
def frontend_home():
    return open("templates/index.html").read()

@app.get("/search", response_class=HTMLResponse)
def frontend_search():
    return open("templates/search.html").read()

@app.get("/booking", response_class=HTMLResponse)
def frontend_booking():
    return open("templates/booking.html").read()

@app.get("/confirmation", response_class=HTMLResponse)
def frontend_confirmation():
    return open("templates/confirmation.html").read()


# Initialize DB tables and sample data
init_db()

# Start background demand simulation (used by pricing engine)
start_demand_simulator()


# ---------------------------------------------------------
# Helper functions
# ---------------------------------------------------------

def row_to_flight(row: sqlite3.Row) -> Flight:
    """Convert SQLite row to Flight Pydantic model."""
    return Flight(
        id=row[0],
        flight_no=row[1],
        origin=row[2],
        destination=row[3],
        departure_date=row[4],
        departure_time=row[5],
        arrival_time=row[6],
        duration_minutes=row[7],
        base_price=row[8],
        seats_total=row[9],
        seats_available=row[10],
        airline=row[11],
    )


def row_to_booking(row: sqlite3.Row) -> Booking:
    """Convert SQLite row to Booking Pydantic model."""
    return Booking(
        id=row[0],
        pnr=row[1],
        flight_id=row[2],
        passenger_name=row[3],
        passenger_email=row[4],
        passenger_phone=row[5],
        seat_number=row[6],
        status=row[7],
        price_paid=row[8],
        booked_at=row[9],
    )


def generate_pnr() -> str:
    """Generate a simple unique-ish PNR."""
    now = datetime.now()
    date_str = now.strftime("%Y%m%d")
    rand_part = random.randint(100, 999)
    letters = "".join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(2))
    return f"PNR{date_str}-{letters}{rand_part}"


# ---------------------------------------------------------
# Basic health / home endpoints
# ---------------------------------------------------------

@app.get("/home")
def read_root():
    return {"message": "Welcome to the flight booking system backend"}


@app.get("/health")
def health_check():
    """Simple health endpoint + counts from DB."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM flights")
    total_flights = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM bookings")
    total_bookings = cursor.fetchone()[0]

    conn.close()

    return {
        "status": "healthy",
        "total_flights": total_flights,
        "total_bookings": total_bookings,
    }


# ---------------------------------------------------------
# Module 1 + 2: Flight search + dynamic pricing
# ---------------------------------------------------------

@app.get("/flights", response_model=List[Flight])
def list_flights(
    sort_by: Optional[str] = Query(
        default=None,
        description="Optional sort: 'price' or 'duration'"
    )
):
    """
    Returns all flights with dynamic price computed per flight.
    Mimics a real-world search response.
    """
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = "SELECT * FROM flights"
    if sort_by == "price":
        query += " ORDER BY base_price ASC"
    elif sort_by == "duration":
        query += " ORDER BY duration_minutes ASC"

    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    flights: List[Flight] = []
    for row in rows:
        f = row_to_flight(row)
        f.dynamic_price = calculate_dynamic_price(
            base_price=f.base_price,
            seats_available=f.seats_available,
            seats_total=f.seats_total,
            departure_date=f.departure_date,
        )
        flights.append(f)

    return flights


@app.get("/flights/search", response_model=List[Flight])
def search_flights(
    origin: str = Query(..., min_length=3, max_length=3),
    destination: str = Query(..., min_length=3, max_length=3),
    departure_date: str = Query(..., pattern=r"^\d{4}-\d{2}-\d{2}$"),
    sort_by: Optional[str] = Query(default=None)
):
    """
    Search for flights with filters:
    - origin, destination, date (required)
    - sort_by price or duration (optional)
    Shows dynamic price in results.
    """
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = """
        SELECT * FROM flights
        WHERE origin = ?
          AND destination = ?
          AND departure_date = ?
    """
    if sort_by == "price":
        query += " ORDER BY base_price ASC"
    elif sort_by == "duration":
        query += " ORDER BY duration_minutes ASC"

    cursor.execute(
        query,
        [origin.upper(), destination.upper(), departure_date]
    )
    rows = cursor.fetchall()
    conn.close()

    flights: List[Flight] = []
    for row in rows:
        f = row_to_flight(row)
        f.dynamic_price = calculate_dynamic_price(
            base_price=f.base_price,
            seats_available=f.seats_available,
            seats_total=f.seats_total,
            departure_date=f.departure_date,
        )
        flights.append(f)

    return flights


@app.post("/external/sync", response_model=int)
def sync_external_flights():
    """
    Simulate pulling flights from an external airline API and storing them.
    Returns number of new flights inserted.
    """
    external = get_external_airline_data()
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    inserted = 0
    for f in external:
        cursor.execute(
            "SELECT COUNT(*) FROM flights WHERE flight_no = ? AND departure_date = ?",
            (f["flight_no"], f["departure_date"])
        )
        exists = cursor.fetchone()[0]

        if exists == 0:
            cursor.execute(
                """
                INSERT INTO flights (
                    flight_no, origin, destination,
                    departure_date, departure_time, arrival_time,
                    duration_minutes, base_price,
                    seats_total, seats_available, airline
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    f["flight_no"], f["origin"], f["destination"],
                    f["departure_date"], f["departure_time"], f["arrival_time"],
                    f["duration_minutes"], f["base_price"],
                    f["seats_total"], f["seats_available"], f["airline"],
                )
            )
            inserted += 1

    conn.commit()
    conn.close()
    return inserted


# ---------------------------------------------------------
# Module 3: Booking workflow & transaction management
# ---------------------------------------------------------

@app.post(
    "/bookings",
    response_model=Booking,
    status_code=status.HTTP_201_CREATED,
)
def create_booking(booking_req: BookingCreate):
    """
    Multi-step booking flow:
    1. Flight & seat selection (flight_id)
    2. Passenger info (from BookingCreate)
    3. Simulated payment (success/fail)
    Uses DB transaction for concurrency-safe seat reservations.
    """
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        # Start transaction (locks relevant rows)
        cursor.execute("BEGIN IMMEDIATE")

        # Step 1: check flight & seat availability
        cursor.execute("SELECT * FROM flights WHERE id = ?", (booking_req.flight_id,))
        flight_row = cursor.fetchone()

        if flight_row is None:
            cursor.execute("ROLLBACK")
            raise HTTPException(status_code=404, detail="Flight not found")

        flight = row_to_flight(flight_row)

        if flight.seats_available <= 0:
            cursor.execute("ROLLBACK")
            raise HTTPException(status_code=400, detail="No seats available on this flight")

        # Step 2: compute dynamic price at booking-time
        dynamic_price = calculate_dynamic_price(
            base_price=flight.base_price,
            seats_available=flight.seats_available,
            seats_total=flight.seats_total,
            departure_date=flight.departure_date,
        )

        # Step 3: simulated payment
        payment_success = random.choice([True, True, False])  # ~66% success
        status_str = "CONFIRMED" if payment_success else "FAILED"

        if payment_success:
            # decrement seat count atomically
            cursor.execute(
                "UPDATE flights SET seats_available = seats_available - 1 WHERE id = ?",
                (booking_req.flight_id,)
            )

        # Insert booking with PNR
        pnr = generate_pnr()
        booked_at = datetime.now().isoformat(timespec="seconds")

        cursor.execute(
            """
            INSERT INTO bookings (
                pnr, flight_id, passenger_name, passenger_email,
                passenger_phone, seat_number, status, price_paid, booked_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                pnr,
                booking_req.flight_id,
                booking_req.passenger_name,
                booking_req.passenger_email,
                booking_req.passenger_phone,
                booking_req.seat_number,
                status_str,
                dynamic_price,
                booked_at,
            )
        )

        booking_id = cursor.lastrowid
        cursor.execute("COMMIT")

    except Exception:
        cursor.execute("ROLLBACK")
        conn.close()
        raise

    conn.close()

    # Fetch created booking for response
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookings WHERE id = ?", (booking_id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        raise HTTPException(status_code=500, detail="Booking not found after creation")

    return row_to_booking(row)


@app.get("/bookings/{pnr}", response_model=Booking)
def get_booking(pnr: str):
    """Retrieve a booking using its PNR."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM bookings WHERE pnr = ?", (pnr,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Booking not found")

    return row_to_booking(row)


@app.get("/bookings/history", response_model=List[Booking])
def booking_history(passenger_email: str = Query(...)):
    """
    Retrieve all bookings for a given passenger email.
    Acts like 'booking history' screen.
    """
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM bookings WHERE passenger_email = ? ORDER BY booked_at DESC",
        (passenger_email,)
    )
    rows = cursor.fetchall()
    conn.close()

    return [row_to_booking(r) for r in rows]


@app.post("/bookings/{pnr}/cancel", response_model=Booking)
def cancel_booking(pnr: str):
    """
    Cancel a CONFIRMED booking:
    - booking status set to CANCELLED
    - seat returned to flights.seats_available
    Uses DB transaction for safety.
    """
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        cursor.execute("BEGIN IMMEDIATE")

        cursor.execute("SELECT * FROM bookings WHERE pnr = ?", (pnr,))
        row = cursor.fetchone()

        if row is None:
            cursor.execute("ROLLBACK")
            raise HTTPException(status_code=404, detail="Booking not found")

        booking = row_to_booking(row)

        if booking.status == "CANCELLED":
            cursor.execute("ROLLBACK")
            raise HTTPException(status_code=400, detail="Booking already cancelled")

        if booking.status != "CONFIRMED":
            cursor.execute("ROLLBACK")
            raise HTTPException(
                status_code=400,
                detail=f"Cannot cancel booking with status {booking.status}"
            )

        # Return seat to flight
        cursor.execute(
            "UPDATE flights SET seats_available = seats_available + 1 WHERE id = ?",
            (booking.flight_id,)
        )

        # Update booking status
        cursor.execute(
            "UPDATE bookings SET status = ? WHERE pnr = ?",
            ("CANCELLED", pnr)
        )

        cursor.execute("COMMIT")

    except Exception:
        cursor.execute("ROLLBACK")
        conn.close()
        raise

    conn.close()

    # Fetch updated booking
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookings WHERE pnr = ?", (pnr,))
    updated_row = cursor.fetchone()
    conn.close()

    return row_to_booking(updated_row)
