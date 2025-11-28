Flight Booking Simulator - README 


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

