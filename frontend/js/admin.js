async function loadStats() {
    try {
        console.log("Attempting to fetch data from:", `${API_BASE}/admin/analytics`);
        
        // Fetch data using the global API_BASE from api.js
        const res = await fetch(`${API_BASE}/admin/analytics`);
        
        if (!res.ok) {
            throw new Error(`Server returned status: ${res.status}`);
        }

        const data = await res.json();
        console.log("Admin Data Received:", data); // Check Console (F12) to see this

        // --- 1. Update Text Stats ---
        document.getElementById("totalRev").innerText = "₹" + (data.total_revenue || 0).toLocaleString();
        document.getElementById("totalBook").innerText = data.total_bookings || 0;
        
        const avg = data.total_bookings > 0 ? Math.round(data.total_revenue / data.total_bookings) : 0;
        document.getElementById("avgPrice").innerText = "₹" + avg.toLocaleString();

        // --- 2. Render Bar Chart (Revenue) ---
        const ctx1 = document.getElementById('revenueChart');
        if (ctx1) {
            new Chart(ctx1, {
                type: 'bar',
                data: {
                    labels: Object.keys(data.airline_revenue || {}), 
                    datasets: [{
                        label: 'Revenue (₹)',
                        data: Object.values(data.airline_revenue || {}),
                        backgroundColor: ['#ff4d88', '#3b82f6', '#10b981', '#f59e0b'],
                        borderRadius: 5
                    }]
                },
                options: { scales: { y: { beginAtZero: true } } }
            });
        }

        // --- 3. Render Pie Chart (Class Distribution) ---
        const ctx2 = document.getElementById('classChart');
        if (ctx2) {
            new Chart(ctx2, {
                type: 'doughnut',
                data: {
                    labels: ['Economy', 'Business'],
                    datasets: [{
                        data: [
                            data.class_distribution?.Economy || 0, 
                            data.class_distribution?.Business || 0
                        ],
                        backgroundColor: ['#e2e8f0', '#f59e0b'],
                        hoverOffset: 4
                    }]
                }
            });
        }

    } catch (e) {
        console.error("Error loading stats:", e);
        alert("Could not load admin data. Ensure Backend is running on port 8000!");
    }
}

// Load stats when the page finishes loading
document.addEventListener("DOMContentLoaded", loadStats);