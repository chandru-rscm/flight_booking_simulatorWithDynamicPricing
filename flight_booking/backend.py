# flight_booking/backend.py

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from .data_seed import seed_data
import random

from .db import get_db, engine
from .models import Flight, Booking, Base
from .pricing_engine import calculate_dynamic_price
from .schemas import BookingRequest

app = FastAPI(
    title="Flight Booking Simulator with Dynamic Pricing",
    description="Infosys Internship Project | Milestone 3",
)

Base.metadata.create_all(bind=engine)

@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    seed_data()



# -----------------------------
# Utility
# -----------------------------
def generate_pnr():
    return "PNR" + str(random.randint(10000000, 99999999))


# -----------------------------
# 0) HEALTH CHECK (IMPORTANT)
# -----------------------------
@app.get("/health")
def health_check():
    return {
        "status": "UP",
        "service": "Flight Booking Simulator",
        "milestone": 3
    }


# -----------------------------
# 1) LIST / SEARCH FLIGHTS
# -----------------------------
@app.get("/flights")
def list_flights(
    origin: str | None = Query(None),
    destination: str | None = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Flight)

    if origin:
        query = query.filter(Flight.origin_airport.has(code=origin))
    if destination:
        query = query.filter(Flight.destination_airport.has(code=destination))

    flights = query.all()
    response = []

    for f in flights:
        price = calculate_dynamic_price(
            f.base_price,
            f.available_seats,
            f.total_seats,
            f.departure_datetime,
            f.demand_level
        )

        response.append({
            "flight_id": f.id,
            "flight_number": f.flight_number,
            "origin": f.origin_airport.code,
            "destination": f.destination_airport.code,
            "departure": f.departure_datetime,
            "arrival": f.arrival_datetime,
            "dynamic_price": price,
            "available_seats": f.available_seats
        })

    return response


# -----------------------------
# 2) GET PRICE OF A FLIGHT
# -----------------------------
@app.get("/flights/{flight_id}/price")
def get_flight_price(flight_id: int, db: Session = Depends(get_db)):
    flight = db.query(Flight).filter(Flight.id == flight_id).first()
    if not flight:
        raise HTTPException(404, "Flight not found")

    price = calculate_dynamic_price(
        flight.base_price,
        flight.available_seats,
        flight.total_seats,
        flight.departure_datetime,
        flight.demand_level
    )

    return {
        "flight_id": flight.id,
        "price": price,
        "available_seats": flight.available_seats
    }


# -----------------------------
# 3) CREATE BOOKING
# -----------------------------
@app.post("/booking")
def create_booking(request: BookingRequest, db: Session = Depends(get_db)):
    flight = (
        db.query(Flight)
        .filter(Flight.id == request.flight_id)
        .with_for_update()
        .first()
    )

    if not flight:
        raise HTTPException(404, "Flight not found")

    if flight.available_seats <= 0:
        raise HTTPException(400, "No seats available")

    flight.available_seats -= 1

    final_price = calculate_dynamic_price(
        flight.base_price,
        flight.available_seats,
        flight.total_seats,
        flight.departure_datetime,
        flight.demand_level
    )

    booking = Booking(
        flight_id=flight.id,
        passenger_name=f"{request.passenger.first_name} {request.passenger.last_name}",
        seat_no=request.seat_no,
        price=final_price,
        status="PENDING_PAYMENT",
        pnr=generate_pnr()
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)

    return {
        "message": "Seat reserved successfully",
        "pnr": booking.pnr,
        "price": booking.price,
        "status": booking.status
    }


# -----------------------------
# 4) PAYMENT SIMULATION
# -----------------------------
@app.post("/booking/pay/{pnr}")
def pay_booking(pnr: str, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.pnr == pnr).first()

    if not booking:
        raise HTTPException(404, "Booking not found")

    if booking.status == "CANCELLED":
        raise HTTPException(400, "Booking cancelled")

    success = random.choice([True, True, False])

    booking.status = "CONFIRMED" if success else "PAYMENT_FAILED"
    db.commit()

    return {
        "pnr": booking.pnr,
        "payment_status": booking.status
    }


# -----------------------------
# 5) GET BOOKING DETAILS
# -----------------------------
@app.get("/booking/{pnr}")
def get_booking(pnr: str, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.pnr == pnr).first()
    if not booking:
        raise HTTPException(404, "Booking not found")

    return {
        "pnr": booking.pnr,
        "passenger": booking.passenger_name,
        "flight_id": booking.flight_id,
        "seat_no": booking.seat_no,
        "price": booking.price,
        "status": booking.status,
        "created_at": booking.created_at
    }


# -----------------------------
# 6) LIST ALL BOOKINGS
# -----------------------------
@app.get("/bookings")
def list_bookings(db: Session = Depends(get_db)):
    bookings = db.query(Booking).all()
    return [
        {
            "pnr": b.pnr,
            "flight_id": b.flight_id,
            "passenger": b.passenger_name,
            "seat": b.seat_no,
            "status": b.status,
            "price": b.price
        }
        for b in bookings
    ]


# -----------------------------
# 7) CANCEL BOOKING
# -----------------------------
@app.delete("/booking/{pnr}")
def cancel_booking(pnr: str, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.pnr == pnr).first()
    if not booking:
        raise HTTPException(404, "Booking not found")

    if booking.status == "CANCELLED":
        return {"message": "Already cancelled"}

    flight = db.query(Flight).filter(Flight.id == booking.flight_id).first()
    flight.available_seats += 1

    booking.status = "CANCELLED"
    db.commit()

    return {"message": f"Booking {pnr} cancelled"}
