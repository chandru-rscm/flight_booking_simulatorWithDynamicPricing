// LocalHost link
//const API_BASE = "http://127.0.0.1:8000"; 

// Render link
const API_BASE = "https://skybook-app.onrender.com"; 

async function apiGet(path) {
    try {
        const cleanPath = path.startsWith('/') ? path : `/${path}`;
        
        const res = await fetch(`${API_BASE}${cleanPath}`);
        if (!res.ok) throw new Error(`API error: ${res.status}`);
        return await res.json();
    } catch (e) {
        console.error("API Call Failed:", e);
        throw e;
    }
}