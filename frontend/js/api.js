// OPTION 1: Localhost (Use this if your backend is running in a terminal on your PC)
const API_BASE = "http://127.0.0.1:8000"; 

// OPTION 2: Live Server (Use this if your backend is deployed online)
// const API_BASE = "https://skybook-app.onrender.com"; 

async function apiGet(path) {
    try {
        // Ensure we don't end up with double slashes (e.g., //admin)
        const cleanPath = path.startsWith('/') ? path : `/${path}`;
        
        const res = await fetch(`${API_BASE}${cleanPath}`);
        if (!res.ok) throw new Error(`API error: ${res.status}`);
        return await res.json();
    } catch (e) {
        console.error("API Call Failed:", e);
        // We throw the error so the calling function handles the alert
        throw e;
    }
}