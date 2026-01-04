// OLD (Localhost)
//const API_BASE = "http://127.0.0.1:8000";

// NEW (Live Render URL) - Use YOUR specific link
const API_BASE = "https://flight-backend-d2cb.onrender.com";

// Global Variables
let currentClass = 'economy'; 
let baseDynamicPrice = 0;
let flightData = null;

document.addEventListener("DOMContentLoaded", async () => {
    const flightId = localStorage.getItem("booking_flight_id");
    const travelDateStr = localStorage.getItem("booking_date");
    const infoDiv = document.getElementById("flightInfo");
    
    if (!flightId || !travelDateStr) {
        alert("Session expired.");
        window.location.href = "search.html";
        return;
    }

    // 1. Fetch Flight
    try {
        const res = await fetch(`${API_BASE}/flights`);
        const flights = await res.json();
        flightData = flights.find(f => f.flight_id == flightId);
        
        if (!flightData) throw new Error("Flight not found");

        // --- CALL WEATHER WIDGET HERE ---
        loadWeather(flightData.destination);

        baseDynamicPrice = flightData.dynamic_price;

        // Render Initial Info
        const dateObj = new Date(travelDateStr);
        const displayDate = dateObj.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' });

        infoDiv.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h2 style="margin: 0; color: #333; font-size: 24px;">${flightData.flight_number}</h2>
                    <p style="font-size: 14px; color: #777;">${flightData.origin} ➝ ${flightData.destination}</p>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 10px; color: #999;">BASE FARE</div>
                    <span id="totalPriceDisplay" style="font-size: 24px; font-weight: 800; color: #ff4d88;">&#8377;${baseDynamicPrice}</span>
                </div>
            </div>
            <div style="margin-top: 10px; font-size: 13px; color: #555;">
                📅 <strong>${displayDate}</strong>
            </div>
            <hr style="margin: 15px 0; border: 0; border-top: 1px dashed #eee;">
        `;

        // Render default map (Economy)
        renderSeatMap();

    } catch (e) {
        infoDiv.innerHTML = "<p style='color:red'>Error loading flight.</p>";
        console.error(e);
    }

    // 2. Booking Confirmation
    const confirmBtn = document.getElementById("confirmBooking");
    confirmBtn.onclick = async () => {
        const fullName = document.getElementById("passengerName").value.trim();
        const seatNo = document.getElementById("selectedSeatVal").value;
        
        if (!fullName) { alert("Please enter Passenger Name"); return; }

        confirmBtn.innerText = "Processing...";
        confirmBtn.disabled = true;

        const nameParts = fullName.split(" ");

        try {
            const payload = {
                flight_id: parseInt(flightId),
                seat_no: seatNo, // e.g. "2A" or "12A"
                travel_date: travelDateStr,
                passenger: {
                    first_name: nameParts[0],
                    last_name: nameParts.slice(1).join(" ") || "",
                    age: 25,
                    phone: 9876543210
                }
            };

            const res = await fetch(`${API_BASE}/booking`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            if (!res.ok) throw new Error("Booking failed");
            const data = await res.json();
            
            localStorage.setItem("pnr", data.pnr);
            window.location.href = "payments.html";

        } catch (err) {
            alert(err.message);
            confirmBtn.disabled = false;
            confirmBtn.innerText = "Confirm & Pay";
        }
    };
});

// 3. Toggle Logic (Global Function)
window.toggleClass = (cls) => {
    currentClass = cls;
    
    // Update Buttons
    const btnEco = document.getElementById("btnEconomy");
    const btnBiz = document.getElementById("btnBusiness");
    
    if(btnEco) btnEco.className = `class-option ${cls === 'economy' ? 'active' : ''}`;
    if(btnBiz) btnBiz.className = `class-option ${cls === 'business' ? 'active biz-active' : ''}`;
    
    // Reset Selection
    document.getElementById("selectedSeatVal").value = "";
    document.getElementById("displaySeat").innerText = "--";
    document.getElementById("displaySurcharge").innerText = "₹0";
    document.getElementById("confirmBooking").disabled = true;
    document.getElementById("displayClass").innerText = cls.charAt(0).toUpperCase() + cls.slice(1);
    
    // Reset Base Price Display (Visual Only)
    const multiplier = cls === 'business' ? 2.5 : 1.0;
    const newBase = (baseDynamicPrice * multiplier).toFixed(2);
    document.getElementById("totalPriceDisplay").innerHTML = `&#8377;${newBase}`;

    renderSeatMap();
};

// 4. Render Map Function
function renderSeatMap() {
    const seatsGrid = document.getElementById("seatsGrid");
    if (!seatsGrid) return;
    seatsGrid.innerHTML = "";

    if (currentClass === 'economy') {
        // --- ECONOMY LAYOUT (3 - 3) ---
        seatsGrid.style.gridTemplateColumns = "repeat(3, 1fr) 30px repeat(3, 1fr)";
        const rows = 10; 
        const startRow = 12;
        const cols = ['A', 'B', 'C', 'SPACE', 'D', 'E', 'F'];

        for (let i = 0; i < rows; i++) {
            createRow(startRow + i, cols, false);
        }

    } else {
        // --- BUSINESS LAYOUT (2 - 2) ---
        seatsGrid.style.gridTemplateColumns = "repeat(2, 1fr) 50px repeat(2, 1fr)";
        const rows = 4;
        const startRow = 1; 
        // Business usually skips middle seats: A, C (Aisle), D (Aisle), F
        const cols = ['A', 'C', 'SPACE', 'D', 'F']; 

        for (let i = 0; i < rows; i++) {
            createRow(startRow + i, cols, true);
        }
    }
}

// Helper to create a row of seats
function createRow(rowNum, cols, isBusiness) {
    const seatsGrid = document.getElementById("seatsGrid");
    
    cols.forEach(col => {
        if (col === 'SPACE') {
            const spacer = document.createElement("div");
            spacer.className = "aisle-spacer";
            seatsGrid.appendChild(spacer);
            return;
        }

        const seatId = `${rowNum}${col}`;
        const seatDiv = document.createElement("div");
        seatDiv.className = `seat ${isBusiness ? 'business' : ''}`;
        seatDiv.innerText = col;
        seatDiv.title = `${isBusiness ? 'Business' : 'Economy'} - ${rowNum}${col}`;

        // Random Occupancy (30%)
        if (Math.random() < 0.3) {
            seatDiv.classList.add("occupied");
        } else {
            seatDiv.onclick = () => selectSeat(seatDiv, seatId, col, isBusiness);
        }

        seatsGrid.appendChild(seatDiv);
    });
}

// 5. Select Seat Logic
function selectSeat(element, seatId, col, isBusiness) {
    // Clear previous
    document.querySelectorAll(".seat.selected").forEach(s => s.classList.remove("selected"));
    
    // Select new
    element.classList.add("selected");
    document.getElementById("selectedSeatVal").value = seatId;
    document.getElementById("displaySeat").innerText = seatId;
    document.getElementById("confirmBooking").disabled = false;
    document.getElementById("confirmBooking").innerText = "Confirm & Pay";

    // Calculate Price
    let multiplier = isBusiness ? 2.5 : 1.0;
    let surcharge = 0;

    // Surcharge Logic
    if (isBusiness) {
        // Business usually includes everything, but let's add minor surcharge for Window just for fun
        if (col === 'A' || col === 'F') surcharge = 500;
    } else {
        // Economy Surcharges
        if (col === 'A' || col === 'F') surcharge = 200; // Window
        if (col === 'C' || col === 'D') surcharge = 100; // Aisle
    }

    document.getElementById("displaySurcharge").innerText = `+₹${surcharge}`;
    
    // Update Total Display
    const total = ((baseDynamicPrice * multiplier) + surcharge).toFixed(2);
    document.getElementById("totalPriceDisplay").innerHTML = `&#8377;${total}`;
}

// --- WEATHER WIDGET LOGIC ---
function loadWeather(city) {
    const widget = document.getElementById("weatherWidget");
    const cityEl = document.getElementById("weatherCity");
    const tempEl = document.getElementById("weatherTemp");
    const descEl = document.getElementById("weatherDesc");
    const iconEl = document.getElementById("weatherIcon");

    if (!city || !widget) return;

    // 1. Realistic Mock Data (Safe for Demos)
    const weathers = [
        { temp: 28, text: "Cloudy", icon: "☁️" },
        { temp: 32, text: "Sunny", icon: "☀️" },
        { temp: 24, text: "Rainy", icon: "🌧️" },
        { temp: 19, text: "Windy", icon: "💨" },
        { temp: 30, text: "Clear Sky", icon: "🌤️" }
    ];

    // Pick weather based on city name length (simple trick)
    const index = city.length % weathers.length;
    const weather = weathers[index];

    // Special cases for realism
    if (city.includes("Mumbai") || city.includes("Chennai")) {
        weather.temp += 2; // Make it hotter
        weather.text = "Humid";
    }
    if (city.includes("Delhi")) {
        weather.temp += 4; // Hotter
        weather.icon = "☀️";
    }
    if (city.includes("Bengaluru")) {
        weather.temp = 22; // Pleasant
        weather.text = "Cool Breeze";
        weather.icon = "🌬️";
    }

    // 2. Update UI
    cityEl.innerText = city;
    tempEl.innerText = weather.temp + "°C";
    descEl.innerText = weather.text;
    iconEl.innerText = weather.icon;
    
    // Show the widget
    widget.style.display = "flex";
}