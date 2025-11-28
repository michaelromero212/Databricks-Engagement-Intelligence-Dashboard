const API_BASE = "http://localhost:8000/api";

export async function getDashboardData() {
    const res = await fetch(`${API_BASE}/dashboard/data`);
    if (!res.ok) throw new Error("Failed to fetch dashboard data");
    return res.json();
}

export async function getHealth() {
    const res = await fetch(`${API_BASE}/health`);
    if (!res.ok) throw new Error("Health check failed");
    return res.json();
}
