CREATE TABLE IF NOT EXISTS flights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    flight_no TEXT NOT NULL,
    origin TEXT NOT NULL,
    destination TEXT NOT NULL,
    departure TEXT NOT NULL,
    arrival TEXT NOT NULL,
    base_fare REAL NOT NULL,
    total_seats INTEGER NOT NULL,
    seats_available INTEGER NOT NULL,
    airline_name TEXT NOT NULL
);

INSERT INTO flights (
    flight_no, origin, destination, departure, arrival,
    base_fare, total_seats, seats_available, airline_name
) VALUES
('AI1', 'Delhi', 'Mumbai', '2025-03-01 10:00:00', '2025-03-01 12:00:00', 8000, 200, 150, 'Air India'),
('AI2', 'Mumbai', 'Delhi', '2025-03-01 15:00:00', '2025-03-01 17:00:00', 8000, 200, 200, 'Air India'),
('AI3', 'Delhi', 'Chennai', '2025-03-01 09:00:00', '2025-03-01 11:30:00', 9000, 200, 180, 'IndiGo'),
('AI4', 'Chennai', 'Delhi', '2025-03-01 13:00:00', '2025-03-01 15:30:00', 9000, 200, 200, 'IndiGo'),
('AI5', 'Mumbai', 'Chennai', '2025-03-01 12:00:00', '2025-03-01 14:30:00', 6000, 200, 160, 'SpiceJet'),
('AI6', 'Chennai', 'Mumbai', '2025-03-01 16:00:00', '2025-03-01 18:30:00', 7000, 200, 200, 'SpiceJet');
