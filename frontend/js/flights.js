// OLD (Localhost)
//const API_BASE = "http://127.0.0.1:8000";

// NEW (Live Render URL) - Use YOUR specific link
const API_BASE = "https://flight-backend-d2cb.onrender.com/";

// Helper: Calculate duration
function getDuration(depStr, arrStr) {
    const dep = new Date(depStr);
    const arr = new Date(arrStr);
    const diffMs = arr - dep; 
    const diffHrs = Math.floor(diffMs / 3600000);
    const diffMins = Math.round(((diffMs % 3600000) / 60000));
    return `${diffHrs}h ${diffMins}m`;
}

// Helper: Format time
function formatTime(dateStr) {
    return new Date(dateStr).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

document.addEventListener("DOMContentLoaded", () => {
    const fromSelect = document.getElementById("from");
    const toSelect = document.getElementById("to");
    const searchBtn = document.getElementById("searchBtn");
    const resultsDiv = document.getElementById("results");

    // 1. Prevent selecting same city
    const handleSelectionChange = () => {
        const fromVal = fromSelect.value;
        const toVal = toSelect.value;
        Array.from(toSelect.options).forEach(opt => opt.disabled = (opt.value === fromVal && opt.value !== ""));
        Array.from(fromSelect.options).forEach(opt => opt.disabled = (opt.value === toVal && opt.value !== ""));
    };

    fromSelect.addEventListener("change", handleSelectionChange);
    toSelect.addEventListener("change", handleSelectionChange);

    // 2. Search Button Click
    searchBtn.addEventListener("click", async () => {
        const from = fromSelect.value;
        const to = toSelect.value;
        const dateInput = document.getElementById("travelDate").value;

        if (!from || !to || !dateInput) {
            alert("Please select Origin, Destination, and Travel Date.");
            return;
        }

        // Validate Date
        const selectedDate = new Date(dateInput);
        const today = new Date();
        today.setHours(0,0,0,0);
        if (selectedDate < today) {
            alert("You cannot book flights in the past!");
            return;
        }

        resultsDiv.innerHTML = `
            <div style="text-align: center; color: #777; padding: 20px;">
                <p>Checking availability for ${dateInput}...</p>
            </div>`;

        try {
            // --- UPDATED: Pass date to Backend ---
            const res = await fetch(`${API_BASE}/flights?origin=${from}&destination=${to}&date=${dateInput}`);
            
            if (!res.ok) throw new Error("API Response was not OK");
            const flights = await res.json();

            resultsDiv.innerHTML = "";

            if (flights.length === 0) {
                showNoResults();
                return;
            }

            let flightsFound = false;

            flights.forEach(flight => {
                // --- 75% AVAILABILITY LOGIC ---
                // Randomly skip 25% of flights to simulate "Not Scheduled on this day"
                if (Math.random() > 0.75) {
                    return; 
                }

                flightsFound = true;

                const duration = getDuration(flight.departure, flight.arrival);
                const depTime = formatTime(flight.departure);
                const arrTime = formatTime(flight.arrival);

                const card = document.createElement("div");
                card.className = "flight-card"; 

                card.innerHTML = `
                    <div class="flight-route">
                        <div style="margin-bottom: 5px;">
                            <h3 style="display:inline; font-size: 20px;">${flight.flight_number}</h3>
                            <span style="font-size:12px; background:#e0f7fa; color:#006064; padding:3px 10px; border-radius:15px; margin-left:10px; font-weight: 600;">
                                ⏱ ${duration}
                            </span>
                        </div>

                        <div style="display: flex; align-items: center; gap: 20px; color: #555; margin-top: 10px;">
                            <div style="text-align: center;">
                                <div style="font-size:18px; font-weight:bold; color: #333;">${depTime}</div>
                                <div style="font-size:12px; color:#888;">${flight.origin}</div>
                            </div>
                            <div style="color:#ddd; font-size: 20px;">➝</div>
                            <div style="text-align: center;">
                                <div style="font-size:18px; font-weight:bold; color: #333;">${arrTime}</div>
                                <div style="font-size:12px; color:#888;">${flight.destination}</div>
                            </div>
                        </div>

                        <p style="margin-top: 10px; font-size: 13px; color: #aaa;">
                            Non-stop • Seats: ${flight.available_seats}
                        </p>
                    </div>
                    
                    <div class="flight-meta">
                        <span class="price-tag">₹${flight.dynamic_price}</span>
                        <button class="book-btn" onclick="bookFlight(${flight.flight_id}, '${dateInput}')">
                            Book Now
                        </button>
                    </div>
                `;
                resultsDiv.appendChild(card);
            });

            if (!flightsFound) {
                resultsDiv.innerHTML = `
                    <div style="text-align: center; padding: 40px; color: #888; background: white; border-radius: 12px;">
                        <h3>No flights available 📅</h3>
                        <p>All flights on this route are sold out or not scheduled for <b>${dateInput}</b>.</p>
                        <p>Try searching for the next day.</p>
                    </div>`;
            }

        } catch (e) {
            console.error(e);
            resultsDiv.innerHTML = `<p style="text-align:center; color:red;">Server Error.</p>`;
        }
    });
});

function showNoResults() {
    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = `
        <div style="text-align: center; padding: 40px; color: #888; background: white; border-radius: 12px;">
            <h3>No flights found 😕</h3>
            <p>Try changing your airports or date.</p>
        </div>`;
}

// 3. Book Function
window.bookFlight = (id, date) => {
    localStorage.setItem("booking_flight_id", id);
    localStorage.setItem("booking_date", date); 
    window.location.href = "booking.html";
};