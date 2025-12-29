Flight Booking Simulator with Dynamic Pricing
Milestones 1 to 3

Project Overview
This project is a Flight Booking Simulator developed to demonstrate how real-world airline booking systems work using dynamic pricing and REST APIs. The system allows users to search for flights, view dynamically calculated prices, book seats, simulate payments, and cancel bookings.

The project follows Agile methodology and is developed milestone-wise with proper sprint planning, testing, and retrospection.

Technology Stack
Backend Framework: FastAPI
Programming Language: Python
Database: SQLite
API Style: REST APIs
Development Methodology: Agile (Scrum)

System Architecture
The system follows a client-server architecture.
The frontend (static HTML/JS) communicates with the backend through REST APIs.
The backend handles business logic, pricing calculation, and database operations using SQLite.

Milestone 1: Core Flight Search and Data Setup

Objective
To create the foundational backend structure and APIs for flight data management.

Implemented Features

Designed relational database schema for flights and bookings

Created SQLite database

Seeded initial flight data

Implemented API to fetch all flights

Implemented API to fetch flight details by flight ID

Outcome
A stable backend capable of serving flight information through REST APIs.

Milestone 2: Dynamic Pricing Engine

Objective
To simulate real-time dynamic pricing similar to airline booking systems.

Implemented Features

Developed a pricing engine module

Implemented demand-based pricing logic

Adjusted prices based on seat availability

Created API to fetch dynamically calculated flight prices

Outcome
Flight prices change dynamically based on demand and availability, simulating real airline behavior.

Milestone 3: Booking, Payment, and Cancellation

Objective
To complete the full booking lifecycle.

Implemented Features

Flight booking API with seat availability validation

PNR generation for each booking

Payment simulation API with success and failure scenarios

Booking cancellation API

Seat restoration on cancellation

Proper error handling for invalid PNRs and no-seat conditions

Outcome
A complete backend flow covering search, booking, payment, and cancellation.

API Endpoints Summary

GET /flights
Fetches all available flights

GET /flights/{id}
Fetches details of a specific flight

GET /flights/{id}/price
Returns dynamically calculated price

POST /booking
Creates a new booking and generates PNR

POST /booking/pay/{pnr}
Simulates payment for a booking

DELETE /booking/{pnr}
Cancels an existing booking

Testing

APIs tested manually through browser and local requests

Edge cases handled such as:

No seat availability

Invalid booking reference

Payment failure scenarios

Test cases documented as part of Agile Test Plan

Agile Methodology

The project follows Agile Scrum practices.
Product backlog was created for each feature.
Work was completed sprint-wise based on milestones.
Daily stand-up updates and sprint retrospectives were documented.

Although the project is part of a team-based Agile setup, the backend development, pricing logic, and API testing were completed as an individual contribution.

Key Learnings

REST API development using FastAPI

Database schema design for booking systems

Implementation of dynamic pricing algorithms

Applying Agile practices in a real project

Handling real-world edge cases in backend systems

How to Run the Backend

Activate the virtual environment.
Run the FastAPI server using uvicorn.

The backend will be available at http://127.0.0.1:8000

Future Enhancements

Complete frontend integration

User authentication and authorization

Seat selection interface

Cloud deployment
