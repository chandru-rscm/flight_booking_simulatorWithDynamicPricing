Flight Booking Simulator - README 

This project implements a complete flight booking system in four milestones. Each milestone adds new features step by step.

------------------------------------------------------------
Milestone 1: Core Flight Search & Data Management
------------------------------------------------------------

What we did:
- Created a SQLite database.
- Added a flights table containing:
  flight number, origin, destination, date, timings, prices, seat count.
- Built backend APIs using FastAPI:
  /flights  -> list all flights
  /flights/search  -> search flights by origin, destination, date
  /external/sync  -> add sample external airline data
- Implemented search filtering, sorting, and input validation.

Purpose:
To create a strong backend foundation with proper flight data and search.

------------------------------------------------------------
Milestone 2: Dynamic Pricing Engine
------------------------------------------------------------

What we did:
- Made a separate file pricing.py.
- Implemented a dynamic airfare calculation using:
  remaining seats, time until departure, demand levels, base fare tiers.
- Built demand_simulator.py to simulate changing demand every 30 seconds.
- Updated flight search and listing to show dynamic prices.

Purpose:
To make the pricing behave like real airlines which change cost based on demand and timing.

------------------------------------------------------------
Milestone 3: Booking Workflow & Transaction Management
------------------------------------------------------------

What we did:
- Added a bookings table in the database.
- Built the full booking flow:
  1. Flight selection
  2. Enter passenger details
  3. Simulated payment (success or fail)
  4. PNR generation
- Ensured concurrency safety using database transactions.
- Added booking cancellation and booking history.
- APIs implemented:
  POST /bookings
  GET /bookings/{pnr}
  POST /bookings/{pnr}/cancel
  GET /bookings/history

Purpose:
To implement realistic airline booking behavior with safe seat updates and proper status tracking.

------------------------------------------------------------
Milestone 4: User Interface & API Integration
------------------------------------------------------------

What we did:
- Added a templates/ folder with HTML files.
- Added a static/ folder for CSS and JavaScript.
- Connected frontend to backend using Fetch API.
- Built:
  - Search page
  - Booking page
  - PNR lookup page
  - Cancellation
  - Receipt download
- Integrated the frontend with FastAPI using StaticFiles.

Purpose:
To make the simulator user-friendly and visually usable as a real system.

------------------------------------------------------------
Final Result
------------------------------------------------------------

The project now contains:
- A fully working backend
- Dynamic pricing engine
- Complete booking system
- Concurrency-safe seat reservation
- Simple but functional frontend
- Booking confirmation and receipt download

How to run:
1. Install dependencies (fastapi, uvicorn)
2. Run:  uvicorn backend:app --reload
3. Open: http://127.0.0.1:8000

You now have a complete flight booking simulator end-to-end.
