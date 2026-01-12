✈️ SkyBook - Flight Booking Simulator with Dynamic Pricing  (https://skybook-app.onrender.com/)


Final Project Report (Milestones 1 to 4) Developer: Chandra Mohan RS

1. Project Overview

SkyBook is a comprehensive Full-Stack Flight Booking Application designed to simulate the real-world experience of an airline reservation system. It demonstrates the complete software development lifecycle (SDLC) using Agile Methodology.

The system features a FastAPI backend that handles dynamic pricing logic and database operations, connected to a responsive HTML/JS frontend. Users can search for flights, view real-time prices (which change based on demand), book tickets, simulate payments, and download official PDF boarding passes. The entire application is deployed live on the cloud.

2. Technology Stack
   
Backend Framework: FastAPI (Python)
Frontend: HTML5, CSS3 (Glassmorphism UI), JavaScript (ES6)
Database: SQLite (Relational DB)
API Style: RESTful APIs
Libraries:
  uvicorn (ASGI Server)
  html2pdf.js (PDF Generation)
  fastapi-cors (Cross-Origin Resource Sharing)
Deployment: Render Cloud (Web Service)
Development Methodology: Agile (Scrum)

3. System Architecture
The system follows a Cloud-Based Client-Server Architecture:
1. Client (Frontend): Hosted as a static site; handles user interaction, form validation, and PDF generation.
2. Server (Backend): Hosted on Render; processes API requests, calculates dynamic prices, and manages the SQLite database.
3. Communication: The frontend and backend exchange data via REST APIs over HTTPS, secured with CORS policies.

4. Milestones Achieved

Milestone 1: Core Flight Search & Data Setup
Objective: Establish the backend structure and database schema.
- Designed the relational database schema for Flights and Bookings.
- Created the SQLite database and seeded it with initial flight routes.
- Implemented GET APIs to fetch all flights and specific flight details.

Milestone 2: Dynamic Pricing Engine
Objective: Simulate real-time airline pricing behavior.
- Developed a custom pricing algorithm in Python.
- Logic: Prices increase automatically as seat availability decreases (Demand-Based Pricing).
- Integrated this logic into the /flight/{id}/price endpoint.

Milestone 3: Booking Lifecycle & Payments
Objective: Enable users to book and cancel tickets.
- Implemented POST APIs for booking creation and PNR generation.
- Built a Payment Simulation (Mock Gateway) that validates card details.
- Added Cancellation Logic (DELETE API) that restores seat availability upon cancellation.

Milestone 4: Frontend Integration & Deployment (Final Phase)
Objective: Create a user interface, generate tickets, and deploy to the cloud.
- UI Design: Developed a modern "Glassmorphism" interface for Search, Payment, and Dashboard pages.
- Ticket Generation: Integrated html2pdf.js to generate downloadable PDF Boarding Passes with QR codes.
- My Bookings: Created a dashboard to fetch and view booking history using LocalStorage and APIs.
- Deployment: Deployed the backend to Render Cloud, enabling global access via a public URL.
- Security: Configured CORS (Cross-Origin Resource Sharing) to allow secure communication between the live frontend and backend.

5. API Endpoints Summary
METHOD   ENDPOINT              DESCRIPTION
GET      /flights              Fetches all available flights
GET      /flights/{id}         Fetches details of a specific flight
GET      /flights/{id}/price   Returns dynamically calculated price based on demand
POST     /booking              Creates a new booking and generates a unique PNR
POST     /booking/pay/{pnr}    Simulates payment transaction for a booking
GET      /bookings             Fetches history of all bookings (for Dashboard)
DELETE   /booking/{pnr}        Cancels an existing booking and refunds the seat

6. Agile Methodology & Testing
The project was executed using Scrum practices:
- Sprint Planning: Work was divided into 4 sprints corresponding to the milestones.
- Testing Strategy:
    - Unit Testing: Verified pricing algorithms and PNR generation logic.
    - Integration Testing: Ensured Frontend successfully fetches data from the Live Backend.
    - Edge Case Handling: Managed scenarios like "Server Sleep" latency, Network Errors, and Invalid PNRs.
    - Defect Tracking: Logged and resolved critical issues like CORS errors and PDF clipping.

7. Key Learnings
- Full Stack Integration: Connecting a Python backend with a vanilla JS frontend using fetch().
- Cloud Deployment: Understanding the difference between localhost and public URLs, and managing production environments on Render.
- CORS & Security: Solving browser security restrictions when APIs and Frontends are hosted on different origins.
- Dynamic PDF Generation: Manipulating the DOM to create professional PDF documents client-side.
- Agile Adaptability: Iteratively improving the product based on testing feedback (e.g., adding loading spinners).

8. How to Run (Live & Local)
Option A: Live Demo
- Visit the User Interface: [[click the link](https://skybook-app.onrender.com/)]
- Note: Please wait 30-50 seconds for the backend to wake up if it's the first request.

Option B: Run Locally
1. Backend:
   cd backend
   source venv/bin/activate
   uvicorn app:app --reload
   (Server runs at: http://127.0.0.1:8000)

2. Frontend:
   Open index.html in any web browser.
   Note: Update API_BASE in the JS files to http://127.0.0.1:8000 for local testing.

9. Future Enhancements
- User Authentication: Add Login/Signup with JWT Tokens.
- Email Notifications: Send the PDF ticket automatically to the user's email.
- Seat Map: Visual interface to select specific window/aisle seats.


📬 Contact

Author: Chandra Mohan RS - chandramohanrs218@gmail.com // +91 70100 87611
Role: Full Stack Developer (Student)
Project Status: Completed ✅
