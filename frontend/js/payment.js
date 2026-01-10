// OLD (Localhost)
const API_BASE = "http://127.0.0.1:8000";

// NEW (Live Render URL) - Use YOUR specific link
//const API_BASE = "https://flight-backend-d2cb.onrender.com";

document.addEventListener("DOMContentLoaded", async () => {
    const detailsDiv = document.getElementById("bookingDetails");
    const payBtn = document.getElementById("payBtn");
    
    // Payment Method Selectors
    const methodCard = document.getElementById("methodCard");
    const methodUPI = document.getElementById("methodUPI");
    let selectedMethod = "CARD"; // Default

    // --- 1. Load Booking Details ---
    const pnr = localStorage.getItem("pnr");

    if (!pnr) {
        alert("PNR missing. Please book a flight first.");
        window.location.href = "search.html";
        return;
    }

    try {
        const res = await fetch(`${API_BASE}/booking/${pnr}`);
        if (!res.ok) throw new Error("Could not find booking");

        const booking = await res.json();

        // Render Summary
        detailsDiv.innerHTML = `
            <div style="background: #f9f9f9; padding: 20px; border-radius: 12px; border: 1px solid #eee;">
                
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <span style="color: #666; font-size: 14px;">PNR Number</span>
                    <span style="font-weight: 800; color: #333; letter-spacing: 1px;">${booking.pnr}</span>
                </div>
                
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <span style="color: #666; font-size: 14px;">Passenger</span>
                    <span style="font-weight: 600; color: #333;">${booking.passenger}</span>
                </div>

                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <span style="color: #666; font-size: 14px;">Seat</span>
                    <span style="font-weight: 600; color: #333;">${booking.seat_no}</span>
                </div>

                <hr style="border: 0; border-top: 1px dashed #ddd; margin: 15px 0;">

                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: #333; font-weight: 600;">Total Amount</span>
                    <span style="font-size: 24px; font-weight: 800; color: #ff4d88;">&#8377;${booking.price}</span>
                </div>
            </div>
        `;
    } catch (e) {
        detailsDiv.innerHTML = "<p style='color:red;'>Failed to load booking details.</p>";
        payBtn.disabled = true;
    }

    // --- 2. Payment Method Toggle Logic ---
    function updateSelection(type) {
        selectedMethod = type;
        
        // Reset Styles
        const activeStyle = "border: 2px solid #ff4d88; color: #ff4d88; background: #fff0f5; font-weight: bold;";
        const inactiveStyle = "border: 1px solid #eee; color: #999; background: white; font-weight: normal;";

        if (type === 'CARD') {
            methodCard.style.cssText += activeStyle;
            methodUPI.style.cssText += inactiveStyle;
        } else {
            methodUPI.style.cssText += activeStyle;
            methodCard.style.cssText += inactiveStyle;
        }
    }

    methodCard.addEventListener("click", () => updateSelection('CARD'));
    methodUPI.addEventListener("click", () => updateSelection('UPI'));


    // --- 3. Handle Payment Click ---
    payBtn.addEventListener("click", async () => {
        payBtn.innerText = `Processing ${selectedMethod === 'CARD' ? 'Card' : 'UPI'} Payment...`;
        payBtn.disabled = true;

        try {
            const res = await fetch(`${API_BASE}/booking/pay/${pnr}`, {
                method: "POST"
            });

            const result = await res.json();
            
            if (result.payment_status === "CONFIRMED") {
                alert("✅ Payment Successful! Your ticket is confirmed.");
                window.location.href = "mybookings.html";
            } else {
                alert("❌ Payment Failed. Please try again.");
                payBtn.innerText = "Retry Payment";
                payBtn.disabled = false;
            }
        } catch {
            alert("Payment failed. Backend not reachable.");
            payBtn.innerText = "Pay Securely";
            payBtn.disabled = false;
        }
    });
});