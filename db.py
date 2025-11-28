# db.py
import sqlite3
from pathlib import Path

DB_NAME = "flights.db"


def get_connection():
    """
    Create (or open) a SQLite database and return a connection object.
    check_same_thread=False is needed because FastAPI can handle requests in multiple threads.
    """
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    return conn


def init_db():
    """
    Create the flights and bookings tables if they do not exist
    and insert some sample flight data.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # -----------------------------
    # Flights table (Module 1)
    # -----------------------------
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS flights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            flight_no TEXT NOT NULL,
            origin TEXT NOT NULL,
            destination TEXT NOT NULL,
            departure_date TEXT NOT NULL,      -- format: YYYY-MM-DD
            departure_time TEXT NOT NULL,      -- format: HH:MM
            arrival_time TEXT NOT NULL,        -- format: HH:MM
            duration_minutes INTEGER NOT NULL,
            base_price REAL NOT NULL,
            seats_total INTEGER NOT NULL,
            seats_available INTEGER NOT NULL,
            airline TEXT NOT NULL
        );
        """
    )

    # -----------------------------
    # Bookings table (Module 3)
    # -----------------------------
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pnr TEXT NOT NULL UNIQUE,
            flight_id INTEGER NOT NULL,
            passenger_name TEXT NOT NULL,
            passenger_email TEXT NOT NULL,
            passenger_phone TEXT NOT NULL,
            seat_number TEXT,
            status TEXT NOT NULL,          -- e.g. CONFIRMED, CANCELLED, FAILED
            price_paid REAL NOT NULL,
            booked_at TEXT NOT NULL,       -- ISO datetime string
            FOREIGN KEY (flight_id) REFERENCES flights(id)
        );
        """
    )

    # Check if flights table already has data
    cursor.execute("SELECT COUNT(*) FROM flights;")
    count = cursor.fetchone()[0]

    if count == 0:
        # Insert some sample flights
        sample_flights = [
            (
                "AI-101", "DEL", "MUM",
                "2025-12-01", "09:00", "11:05",
                125, 5000.0, 180, 50, "Air India"
            ),
            (
                "6E-202", "DEL", "BLR",
                "2025-12-01", "10:30", "13:00",
                150, 4800.0, 180, 100, "IndiGo"
            ),
            (
                "SG-303", "MUM", "DEL",
                "2025-12-01", "14:00", "16:10",
                130, 4500.0, 180, 75, "SpiceJet"
            ),
            (
                "UK-404", "BLR", "MUM",
                "2025-12-02", "06:30", "08:15",
                105, 4200.0, 160, 60, "Vistara"
            ),
        ]

        cursor.executemany(
            """
            INSERT INTO flights (
                flight_no, origin, destination,
                departure_date, departure_time, arrival_time,
                duration_minutes, base_price,
                seats_total, seats_available, airline
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """,
            sample_flights
        )
        print("Sample flight data inserted into database.")

    conn.commit()
    conn.close()
