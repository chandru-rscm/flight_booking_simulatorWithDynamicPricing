// OLD (Localhost)
//const API_BASE = "http://127.0.0.1:8000";

// NEW (Live Render URL) - Use YOUR specific link
const API_BASE = "https://flight-booking-simulator-y78k.onrender.com/";

async function apiGet(path) {
    try {
        const res = await fetch(API_BASE_URL + path);
        if (!res.ok) throw new Error("API error");
        return await res.json();
    } catch (e) {
        alert("Backend not reachable");
        throw e;
    }
}
