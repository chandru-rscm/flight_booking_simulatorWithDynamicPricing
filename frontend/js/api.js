const API_BASE_URL = "http://127.0.0.1:8000";

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
