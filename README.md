FLIGHT BOOKING SIMULATOR WITH DYNAMIC PRICING
Milestone 1 + Milestone 2

This project is part of the Infosys Interns Full Stack Program.
It implements the backend for a Flight Booking Simulator using Python, FastAPI, SQLAlchemy, and SQLite.

The system supports:

Flight searching

Route and date-based filtering

Sorting results

Dynamic fare calculation

Demand simulation

External airline feed simulation

Milestones 1 and 2 cover the complete backend foundation and pricing engine.

=========================================================
PROJECT OBJECTIVES

Build a backend resembling real airline flight search systems

Implement dynamic pricing based on seat availability, time, and demand

Simulate airline schedule data

Design clean APIs using FastAPI

Implement ORM models using SQLAlchemy

Prepare backend for later booking and UI modules

=========================================================
TECH STACK

Backend Framework: FastAPI
Database: SQLite (via SQLAlchemy ORM)
Programming Language: Python
API Documentation: Swagger / OpenAPI
Environment: Python 3.13

=========================================================
FOLDER STRUCTURE

flight_booking/
backend.py → FastAPI routes
db.py → Database engine, session, Base
models.py → ORM Models (Airline, Airport, Flight)
data_seed.py → Sample data generator
pricing_engine.py → Dynamic pricing logic
demand_simulator.py → Simulated demand and seat updates
flights.db → SQLite database
.gitignore → Repo ignore rules
README.txt → Documentation
myenv/ → Virtual environment (ignored)

=========================================================
MILESTONE 1 – CORE FLIGHT SEARCH & DATA MANAGEMENT

Database Schema Designed

Airlines table (id, code, name)

Airports table (id, code, city, name)

Flights table (flight number, timings, prices, seats, demand level)

Database Setup

SQLite database generated automatically

SQLAlchemy ORM used for table creation

Data Seeding

data_seed.py populates the database with

Sample airlines

Airports

Multiple daily flights

Created FastAPI Endpoints
GET /flights → Get all flights
GET /search → Search flights by origin, destination, date
GET /external/airline-feed → Mock airline data simulation

Input Validation

Airport code format

Date format (YYYY-MM-DD)

Route validation

Empty result handling

=========================================================
MILESTONE 2 – DYNAMIC PRICING ENGINE

Dynamic pricing implemented using real airline-style logic.

Pricing adjustments include:

Remaining Seats
If < 20% → +20%
If < 50% → +10%

Time to Departure
Within 1 day → +25%
Within 3 days → +15%
Within 7 days → +5%

Demand Level
Level 2 → +10%
Level 3 → +25%

Final dynamic price = base price + adjustments.

Demand simulator script updates seats and demand regularly.

=========================================================
DEMAND SIMULATION

demand_simulator.py performs:

Random seat reduction

Random demand level selection

Continuous database updates

This causes flight prices to fluctuate in real time.

=========================================================
API ENDPOINTS

GET /flights
Returns all flights with both base and dynamic price.

GET /search?origin=XXX&destination=YYY&date_str=YYYY-MM-DD
Filters flights based on route and date.
Optional sorting: sort_by=price or sort_by=duration.

GET /external/airline-feed
Simulated third-party airline schedule feed.

=========================================================
HOW TO RUN LOCALLY

Install dependencies
pip install fastapi uvicorn sqlalchemy

Seed the database
python data_seed.py

Run server
uvicorn backend:app --reload

Open Swagger UI
http://127.0.0.1:8000/docs

Run demand simulator (optional)
python demand_simulator.py

=========================================================
NOTES

This repository contains the complete work for both Milestone 1 and Milestone 2.

The backend is fully modular and ready for Milestone 3 (Booking System).

Codebase follows clean structure for professional backend applications.
