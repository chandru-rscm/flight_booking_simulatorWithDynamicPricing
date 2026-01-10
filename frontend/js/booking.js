// OLD (Localhost)
//const API_BASE = "http://127.0.0.1:8000";

// NEW (Live Render URL) - Use YOUR specific link
// NEW (Live Render URL)
const API_BASE = "https://flight-backend-d2cb.onrender.com";

// Global Variables
let currentClass = 'economy'; 
let baseDynamicPrice = 0;
let flightData = null;
let selectedSeats = []; // Array to store multiple selected seats

document.addEventListener("DOMContentLoaded", async () => {
    const flightId = localStorage.getItem("booking_flight_id");
    const travelDateStr = localStorage.getItem("booking_date");
    
    // Check Login
    const userEmail = localStorage.getItem("userEmail") || localStorage.getItem("loggedUser");
    if (!userEmail) {
        alert("Please log in to book a ticket.");
        window.location.href = "login.html";
        return;
    }
    
    if (!flightId || !travelDateStr) {
        alert("Session expired.");
        window.location.href = "search.html";
        return;
    }

    // 1. Initialize Passenger Form (Add first passenger)
    if(document.getElementById("passengersContainer").children.length === 0) {
        addPassengerForm(true); 
    }

    // 2. Fetch Flight Data
    try {
        const res = await fetch(`${API_BASE}/flights`);
        const flights = await res.json();
        flightData = flights.find(f => f.flight_id == flightId);
        
        if (!flightData) throw new Error("Flight not found");

        baseDynamicPrice = flightData.dynamic_price;

        // Update Header Info
        document.getElementById("flightRouteDisplay").innerText = 
            `${flightData.flight_number} • ${flightData.origin} ➝ ${flightData.destination} • ${travelDateStr}`;
        
        updateTotal(); // Initialize pricing
        renderSeatMap(); // Render seats

    } catch (e) {
        console.error(e);
        alert("Error loading flight info");
    }
});

// --- PASSENGER FORM LOGIC ---
function addPassengerForm(isFirst = false) {
    const container = document.getElementById("passengersContainer");
    const div = document.createElement("div");
    div.className = "passenger-card";
    div.innerHTML = `
        <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
            <strong style="color:#334155; font-size:13px;">PASSENGER ${container.children.length + 1}</strong>
            ${!isFirst ? `<span onclick="removePassenger(this)" style="color:#ef4444; cursor:pointer; font-size:12px; font-weight:bold;">✕ Remove</span>` : ''}
        </div>
        <div style="display:flex; gap:15px;">
            <input type="text" class="p-name" placeholder="Full Name" style="flex:2; padding:12px; border:1px solid #e2e8f0; border-radius:8px; outline:none;">
            <input type="number" class="p-age" placeholder="Age" style="flex:1; padding:12px; border:1px solid #e2e8f0; border-radius:8px; outline:none;">
        </div>
    `;
    container.appendChild(div);
    updatePassengerCount();
}

function removePassenger(el) {
    el.parentElement.parentElement.remove();
    updatePassengerCount();
}

function updatePassengerCount() {
    const count = document.getElementById("passengersContainer").children.length;
    // Update text references if any exist
    if(document.getElementById("pCount")) document.getElementById("pCount").innerText = count;
    
    // Reset selections if count changes to ensure validity
    selectedSeats = [];
    renderSeatMap(); 
    updateTotal();
}

// --- SEAT MAP LOGIC ---
function setSeatClass(cls) {
    currentClass = cls;
    
    // Toggle Button Styles
    const btnEco = document.getElementById("btnEco");
    const btnBiz = document.getElementById("btnBiz");
    
    if(btnEco && btnBiz) {
        if(cls === 'economy') {
            btnEco.style.background = '#fff'; btnEco.style.boxShadow = '0 2px 5px rgba(0,0,0,0.1)';
            btnBiz.style.background = 'transparent'; btnBiz.style.boxShadow = 'none';
        } else {
            btnBiz.style.background = '#fcd34d'; btnBiz.style.boxShadow = '0 2px 5px rgba(0,0,0,0.1)';
            btnEco.style.background = 'transparent'; btnEco.style.boxShadow = 'none';
        }
    }

    selectedSeats = [];
    renderSeatMap();
    updateTotal();
}

function getSeatSurcharge(col) {
    // Window: A, F | Aisle: C, D (Economy)
    if (['A', 'F'].includes(col)) return 200;
    if (['C', 'D'].includes(col) && currentClass === 'economy') return 100;
    return 0;
}

function renderSeatMap() {
    // FIX: Target 'seatMap' to match HTML ID
    const grid = document.getElementById("seatMap");
    if(!grid) return;
    grid.innerHTML = "";
    
    const rows = currentClass === 'economy' ? 12 : 5;
    // Economy: 3-3 (A,B,C - D,E,F) | Business: 2-2 (A,C - D,F)
    const cols = currentClass === 'economy' ? ['A','B','C', 'SPACE', 'D','E','F'] : ['A','C', 'SPACE', 'D','F'];
    const startRow = currentClass === 'economy' ? 10 : 1;

    // FIX: Dynamic Grid Columns to prevent collapse
    grid.style.gridTemplateColumns = currentClass === 'economy' 
        ? "repeat(3, 1fr) 30px repeat(3, 1fr)" 
        : "repeat(2, 1fr) 50px repeat(2, 1fr)";

    for(let r=0; r<rows; r++) {
        const rowNum = startRow + r;
        cols.forEach(col => {
            if (col === 'SPACE') {
                const spacer = document.createElement("div");
                spacer.className = "aisle"; // CSS handles width
                grid.appendChild(spacer);
                return;
            }

            const seatId = `${rowNum}${col}`;
            const seat = document.createElement("div");
            seat.className = `seat ${currentClass}`;
            seat.innerText = seatId;
            
            // Surcharge Tooltip
            const surcharge = getSeatSurcharge(col);
            const multiplier = currentClass === 'business' ? 2.5 : 1.0;
            const seatCost = Math.round(baseDynamicPrice * multiplier) + surcharge;
            seat.setAttribute("data-price", `₹${seatCost}`);

            // Random Occupancy (Visual only)
            if (Math.random() < 0.25) {
                seat.classList.add("occupied");
            } else {
                seat.onclick = () => toggleSeat(seat, seatId);
            }

            // Restore Selection State
            if(selectedSeats.includes(seatId)) {
                seat.classList.add("selected");
                // Specific fix for Business class color
                if(currentClass === 'business') seat.classList.add("business-selected"); 
            }

            grid.appendChild(seat);
        });
    }
}

function toggleSeat(el, id) {
    const pCount = document.getElementById("passengersContainer").children.length;

    if (selectedSeats.includes(id)) {
        selectedSeats = selectedSeats.filter(s => s !== id);
        el.classList.remove("selected");
    } else {
        if (selectedSeats.length < pCount) {
            selectedSeats.push(id);
            el.classList.add("selected");
        } else {
            alert(`You have ${pCount} passenger(s). Add more passengers to select more seats.`);
        }
    }
    updateTotal();
}

// --- TOTAL & CONFIRM ---
function updateTotal() {
    // If element doesn't exist yet, skip
    if(!document.getElementById("totalFareDisplay")) return;

    const multiplier = currentClass === 'business' ? 2.5 : 1.0;
    
    // Calculate Base (Price * Count)
    const pCount = selectedSeats.length; 
    const baseTotal = Math.round(baseDynamicPrice * multiplier * pCount);
    
    // Calculate Surcharges
    let surchargeTotal = 0;
    selectedSeats.forEach(seat => {
        const col = seat.slice(-1);
        surchargeTotal += getSeatSurcharge(col);
    });

    const finalTotal = baseTotal + surchargeTotal;
    
    // Update UI
    document.getElementById("baseFareDisplay").innerText = `₹${baseTotal}`;
    document.getElementById("surchargeDisplay").innerText = `+₹${surchargeTotal}`;
    document.getElementById("totalFareDisplay").innerText = `₹${finalTotal}`;

    const btn = document.getElementById("payButton");
    const totalPassengers = document.getElementById("passengersContainer").children.length;
    
    if (selectedSeats.length === totalPassengers && totalPassengers > 0) {
        btn.disabled = false;
        btn.style.background = "#ff4d88";
        btn.style.cursor = "pointer";
        btn.innerHTML = `Proceed to Pay <span style="font-size:1.1em">₹${finalTotal}</span>`;
    } else {
        btn.disabled = true;
        btn.style.background = "#cbd5e1";
        btn.style.cursor = "not-allowed";
        const remaining = totalPassengers - selectedSeats.length;
        btn.innerText = remaining > 0 ? `Select ${remaining} more seat(s)` : "Select Seats";
    }
}

async function confirmBooking() {
    const passengers = [];
    const inputs = document.querySelectorAll(".passenger-card");
    
    let valid = true;
    inputs.forEach(card => {
        const name = card.querySelector(".p-name").value;
        const age = card.querySelector(".p-age").value;
        if(!name || !age) valid = false;
        passengers.push({ 
            first_name: name.split(" ")[0], 
            last_name: name.split(" ").slice(1).join(" ") || "", 
            age: parseInt(age) || 0 
        });
    });

    if(!valid) return alert("Please fill all passenger details.");

    const payload = {
        user_email: localStorage.getItem("userEmail") || localStorage.getItem("loggedUser"),
        flight_id: parseInt(localStorage.getItem("booking_flight_id")),
        passengers: passengers,
        seat_class: currentClass,
        travel_date: localStorage.getItem("booking_date"),
        seat_numbers: selectedSeats 
    };

    const btn = document.getElementById("payButton");
    const originalText = btn.innerHTML;
    btn.innerText = "Processing...";
    btn.disabled = true;

    try {
        const res = await fetch(`${API_BASE}/booking/create`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        
        const data = await res.json();
        
        if(res.ok) {
            localStorage.setItem("temp_booking_id", data.booking_id);
            window.location.href = "payments.html";
        } else {
            alert("Booking Failed: " + (data.detail || JSON.stringify(data)));
            btn.innerHTML = originalText;
            btn.disabled = false;
        }
    } catch(e) {
        alert("Server connection failed");
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
}