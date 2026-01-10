from fastapi import FastAPI, Depends, HTTPException, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
import random
from datetime import datetime

# --- IMPORT LOCAL MODULES ---
from data_seed import seed_data
from db import get_db, engine
from models import Flight, Booking, Base, User
from pricing_engine import calculate_dynamic_price
from schemas import BookingRequest, UserSignup, UserLogin, VerifyOTP

app = FastAPI()

# 1. ALLOW CROSS-ORIGIN REQUESTS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

@app.on_event("startup")
def startup_event():
    seed_data()

# --- EMAIL CONFIGURATION (Kept for Ticket Confirmation only) ---
conf = ConnectionConfig(
    MAIL_USERNAME = "chandramohanrs218@gmail.com",
    MAIL_PASSWORD = "xfkc woat qdho ymzh", 
    MAIL_FROM = "chandramohanrs218@gmail.com",
    MAIL_PORT = 465,             
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS = False,       
    MAIL_SSL_TLS = True,         
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

# ==========================================
# AUTH ROUTES (UPDATED: NO OTP)
# ==========================================

@app.post("/auth/signup")
def signup(user: UserSignup, db: Session = Depends(get_db)):
    # Case Insensitive Check
    existing = db.query(User).filter(func.lower(User.email) == user.email.lower()).first()
    if existing: 
        raise HTTPException(400, "User already exists. Please Log In.")
    
    new_user = User(
        email=user.email.lower(), 
        password=user.password, 
        name=user.name, 
        phone=user.phone, 
        dob=user.dob
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "Account created successfully"}

@app.post("/auth/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    # Direct Password Check (No OTP)
    db_user = db.query(User).filter(
        func.lower(User.email) == user.email.lower(), 
        User.password == user.password
    ).first()
    
    if not db_user: 
        raise HTTPException(400, "Invalid email or password.")
    
    # Return user info directly
    return {
        "message": "Login successful", 
        "email": db_user.email, 
        "name": db_user.name
    }

# ==========================================
# FLIGHT ROUTES
# ==========================================

@app.get("/flights")
def list_flights(origin: str | None = Query(None), destination: str | None = Query(None), date: str | None = Query(None), db: Session = Depends(get_db)):
    query = db.query(Flight)
    if origin: query = query.filter(Flight.origin_airport.has(code=origin))
    if destination: query = query.filter(Flight.destination_airport.has(code=destination))
    if date: query = query.filter(func.date(Flight.departure_datetime) == date)
    
    flights = query.all()
    response = []
    
    for f in flights:
        price = calculate_dynamic_price(f.base_price, f.available_seats, f.total_seats, f.departure_datetime, f.demand_level)
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

# ==========================================
# BOOKING ROUTES
# ==========================================

@app.post("/booking/create")
def create_booking(req: BookingRequest, db: Session = Depends(get_db)):
    flight = db.query(Flight).filter(Flight.id == req.flight_id).first()
    if not flight: raise HTTPException(400, "Flight not found")
    
    if len(req.seat_numbers) != len(req.passengers): raise HTTPException(400, "Seat count mismatch")
    if flight.available_seats < len(req.passengers): raise HTTPException(400, "Not enough seats")

    base_price = calculate_dynamic_price(flight.base_price, flight.available_seats, flight.total_seats, flight.departure_datetime, flight.demand_level)
    multiplier = 2.5 if req.seat_class.lower() == "business" else 1.0
    seat_base_cost = base_price * multiplier

    total_surcharge = 0
    for seat in req.seat_numbers:
        col = seat[-1]
        if col in ['A', 'F']: total_surcharge += 200
        elif col in ['C', 'D']: total_surcharge += 100

    total_price = (seat_base_cost * len(req.passengers)) + total_surcharge
    
    p_names = ", ".join([f"{p.first_name} {p.last_name}" for p in req.passengers])
    seats_str = ", ".join(req.seat_numbers)

    new_booking = Booking(
        user_email=req.user_email, 
        flight_id=flight.id, 
        passenger_names=p_names,
        passenger_count=len(req.passengers), 
        seat_numbers=seats_str,
        travel_date=req.travel_date, 
        total_price=round(total_price, 2), 
        status="PENDING_PAYMENT"
    )
    
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    
    return {"booking_id": new_booking.id, "amount": new_booking.total_price}

@app.get("/booking/id/{booking_id}")
def get_booking_by_id(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking: raise HTTPException(404, "Booking not found")
    
    flight = db.query(Flight).filter(Flight.id == booking.flight_id).first()
    
    return {
        "id": booking.id,
        "amount": booking.total_price,
        "passengers": booking.passenger_names,
        "passenger_count": booking.passenger_count,
        "seats": booking.seat_numbers,
        "flight_number": flight.flight_number,
        "origin": flight.origin_airport.city + " (" + flight.origin_airport.code + ")",
        "destination": flight.destination_airport.city + " (" + flight.destination_airport.code + ")",
        "departure_time": flight.departure_datetime.strftime("%H:%M"),
        "travel_date": booking.travel_date,
        "status": booking.status,
        "pnr": booking.pnr
    }

@app.post("/booking/pay/{booking_id}")
async def pay_booking(booking_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking: raise HTTPException(404, "Booking not found")

    pnr = "PNR" + str(random.randint(1000000, 9999999))
    booking.status = "CONFIRMED"
    booking.pnr = pnr
    
    flight = db.query(Flight).filter(Flight.id == booking.flight_id).first()
    flight.available_seats -= booking.passenger_count
    db.commit()

    # Try sending email, but don't crash if it fails
    try:
        email_body = f"""
        <div style="font-family: Arial, sans-serif; padding: 20px; border: 1px solid #eee;">
            <h1 style="color: #ff4d88;">Booking Confirmed!</h1>
            <p>PNR: <b>{pnr}</b></p>
            <p>Flight: {flight.flight_number}</p>
            <p>Passengers: {booking.passenger_names}</p>
            <p>Seats: {booking.seat_numbers}</p>
            <p>Total: Rs. {booking.total_price}</p>
        </div>"""
        
        message = MessageSchema(
            subject=f"Ticket - {pnr}", 
            recipients=[booking.user_email], 
            body=email_body, 
            subtype=MessageType.html
        )
        fm = FastMail(conf)
        background_tasks.add_task(fm.send_message, message)
    except Exception as e:
        print(f"Email failed to send (Ticket generated anyway): {e}")

    return {"status": "SUCCESS", "pnr": pnr}

@app.delete("/booking/{pnr}")
def cancel_booking(pnr: str, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.pnr == pnr).first()
    if not booking:
        raise HTTPException(404, "Booking not found")

    if booking.status == "CANCELLED":
        return {"message": "Already cancelled"}

    # Restore seats
    flight = db.query(Flight).filter(Flight.id == booking.flight_id).first()
    if flight:
        flight.available_seats += booking.passenger_count

    booking.status = "CANCELLED"
    db.commit()

    return {"message": f"Booking {pnr} cancelled"}

@app.get("/my-bookings/{email}")
def get_user_bookings(email: str, db: Session = Depends(get_db)):
    bookings = db.query(Booking).filter(Booking.user_email == email).order_by(Booking.id.desc()).all()
    results = []
    for b in bookings:
        flight = db.query(Flight).filter(Flight.id == b.flight_id).first()
        results.append({
            "pnr": b.pnr,
            "flight_number": flight.flight_number,
            "origin": flight.origin_airport.city,
            "destination": flight.destination_airport.city,
            "travel_date": b.travel_date,
            "passenger_names": b.passenger_names,
            "passenger_count": b.passenger_count,
            "seats": b.seat_numbers,
            "total_price": b.total_price,
            "status": b.status
        })
    return results

# ==========================================
# ADMIN ROUTES
# ==========================================

@app.get("/admin/stats")
def get_admin_stats(db: Session = Depends(get_db)):
    try:
        user_count = db.query(User).count()
        booking_count = db.query(Booking).count()
        
        income_query = db.query(func.sum(Booking.total_price)).filter(Booking.status == "CONFIRMED").scalar()
        total_income = income_query if income_query else 0
        
        flight_count = db.query(Flight).count()

        return {
            "users": user_count,
            "bookings": booking_count,
            "income": total_income,
            "flights": flight_count
        }
    except Exception as e:
        print(f"Stats Error: {e}")
        raise HTTPException(500, "Internal Server Error")

@app.get("/admin/recent-bookings")
def get_recent_bookings(db: Session = Depends(get_db)):
    try:
        bookings = db.query(Booking).order_by(Booking.id.desc()).limit(10).all()
        results = []
        for b in bookings:
            p_name = b.passenger_names.split(",")[0] if b.passenger_names else "Unknown"
            results.append({
                "name": p_name, 
                "pnr": b.pnr or "Pending",
                "price": b.total_price,
                "status": b.status,
                "date": b.travel_date
            })
        return results
    except Exception as e:
        return []