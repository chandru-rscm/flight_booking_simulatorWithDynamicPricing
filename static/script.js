
// SEARCH FLIGHTS
document.addEventListener("DOMContentLoaded", () => {
    let form = document.getElementById("searchForm");
    if (form) {
        form.addEventListener("submit", async (event) => {
            event.preventDefault();

            let origin = document.getElementById("origin").value;
            let destination = document.getElementById("destination").value;
            let date = document.getElementById("date").value;

            let results = document.getElementById("results");
            results.innerHTML = "<p>Searching...</p>";

            try {
                let response = await fetch(
                    `/flights/search?origin=${origin}&destination=${destination}&departure_date=${date}`
                );

                // If API returned an error status
                if (!response.ok) {
                    let err = await response.json();
                    results.innerHTML = `<p style="color:red;">Error: ${err.detail || response.status}</p>`;
                    return;
                }

                let data = await response.json();

                if (!Array.isArray(data) || data.length === 0) {
                    results.innerHTML = "<p>No flights found for given details.</p>";
                    return;
                }

                results.innerHTML = "";
                data.forEach(f => {
                    results.innerHTML += `
                        <div class='card'>
                            <h3>${f.flight_no} - ${f.airline}</h3>
                            <p>${f.origin} → ${f.destination}</p>
                            <p>Date: ${f.departure_date}</p>
                            <p>Departure: ${f.departure_time} | Arrival: ${f.arrival_time}</p>
                            <p>Base Price: ₹${f.base_price}</p>
                            <p><b>Dynamic Price: ₹${f.dynamic_price}</b></p>
                            <button onclick="bookFlight(${f.id})">Book</button>
                        </div>
                        <br>
                    `;
                });

            } catch (e) {
                console.error(e);
                results.innerHTML = "<p style='color:red;'>Network or server error.</p>";
            }
        });
    }
});

// BOOK FLIGHT
async function bookFlight(id) {
    let passenger_name = prompt("Enter passenger name:");
    if (!passenger_name) return;

    let passenger_email = prompt("Enter email:");
    if (!passenger_email) return;

    let passenger_phone = prompt("Enter phone:");
    if (!passenger_phone) return;

    let seat = prompt("Seat number (optional):");

    let body = {
        flight_id: id,
        passenger_name,
        passenger_email,
        passenger_phone,
        seat_number: seat || null
    };

    let response = await fetch("/bookings", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
    });

    let data = await response.json();

    if (!response.ok) {
        alert("Error during booking: " + (data.detail || response.status));
        return;
    }

    if (data.status === "FAILED") {
        alert("Payment failed! Try again.");
        return;
    }

    alert("Booking confirmed! PNR: " + data.pnr);

    // Redirect to confirmation page if you wired it
    window.location.href = `/confirmation?pnr=${data.pnr}`;
}


// FETCH BOOKING BY PNR
async function fetchBooking() {
    let pnr = document.getElementById("pnrInput").value;
    if (!pnr) {
        alert("Enter a PNR");
        return;
    }

    let response = await fetch(`/bookings/${pnr}`);
    let data = await response.json();

    if (!response.ok) {
        alert(data.detail || "Error fetching booking");
        return;
    }

    let div = document.getElementById("bookingDetails");

    div.innerHTML = `
        <h3>Booking Details</h3>
        <p>PNR: ${data.pnr}</p>
        <p>Name: ${data.passenger_name}</p>
        <p>Flight ID: ${data.flight_id}</p>
        <p>Status: ${data.status}</p>
        <button onclick="cancelBooking('${data.pnr}')">Cancel Booking</button>
        <button onclick="downloadReceipt('${data.pnr}')">Download Receipt</button>
    `;
}

// CANCEL BOOKING
async function cancelBooking(pnr) {
    let response = await fetch(`/bookings/${pnr}/cancel`, {
        method: "POST"
    });

    let data = await response.json();

    if (!response.ok) {
        alert(data.detail || "Error cancelling booking");
        return;
    }

    alert("Booking cancelled!");
    location.reload();
}


// DOWNLOAD RECEIPT
async function downloadReceipt(pnrFromButton) {
    let pnr = pnrFromButton;

    let response = await fetch(`/bookings/${pnr}`);
    let data = await response.json();

    if (!response.ok) {
        alert(data.detail || "Error getting receipt");
        return;
    }

    let blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
    let link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `${pnr}-receipt.json`;
    link.click();
}
