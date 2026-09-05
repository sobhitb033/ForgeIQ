const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

function getTokenPayload() {
    const token = localStorage.getItem("access_token");
    if (!token) return null;
    try {
        const p = token.split(".");
        if (p.length !== 3) return null;
        const b64 = p[1].replace(/-/g, "+").replace(/_/g, "/");
        return JSON.parse(atob(b64.padEnd(b64.length + (4 - b64.length % 4) % 4, "=")));
    } catch { return null; }
}
export function getTokenExpiration() { const p = getTokenPayload(); return p?.exp ? p.exp * 1000 : null; }
export function logoutUser() { localStorage.removeItem("access_token"); window.dispatchEvent(new Event("forgeiq:logout")); }
export function isAuthenticated() {
    const token = localStorage.getItem("access_token");
    if (!token) return false;
    const exp = getTokenExpiration();
    if (!exp || Date.now() >= exp) { localStorage.removeItem("access_token"); return false; }
    return true;
}
async function parseResponse(response) { const text = await response.text(); if (!text) return {}; try { return JSON.parse(text); } catch { return { detail: text }; } }
export async function authenticatedFetch(url, options = {}) {
    if (!isAuthenticated()) { logoutUser(); throw new Error("Your session has expired. Please login again."); }
    const token = localStorage.getItem("access_token");
    const response = await fetch(url, { ...options, headers: { ...(options.headers || {}), Authorization: `Bearer ${token}` } });
    if (response.status === 401) { logoutUser(); throw new Error("Your session has expired. Please login again."); }
    return response;
}
export async function registerUser(userData) { const r = await fetch(`${API_BASE_URL}/auth/register`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(userData) }); const d = await parseResponse(r); if (!r.ok) throw new Error(d.detail || "Registration failed"); return d; }
export async function loginUser(email, password) { const f = new URLSearchParams(); f.append("username", email); f.append("password", password); const r = await fetch(`${API_BASE_URL}/auth/login`, { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" }, body: f.toString() }); const d = await parseResponse(r); if (!r.ok) throw new Error(d.detail || "Login failed"); localStorage.setItem("access_token", d.access_token); return d; }
export async function googleLogin(credential) { const r = await fetch(`${API_BASE_URL}/auth/google`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ credential }) }); const d = await parseResponse(r); if (!r.ok) throw new Error(d.detail || "Google login failed"); localStorage.setItem("access_token", d.access_token); return d; }
export async function forgotPassword(email) { const r = await fetch(`${API_BASE_URL}/auth/forgot-password`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ email: email.trim() }) }); const d = await parseResponse(r); if (!r.ok) throw new Error(d.detail || "Failed to send password reset OTP"); return d; }
export async function verifyOTP(email, otp) { const r = await fetch(`${API_BASE_URL}/auth/verify-otp`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ email: email.trim(), otp }) }); const d = await parseResponse(r); if (!r.ok) throw new Error(d.detail || "Invalid or expired OTP"); return d; }
export async function resetPassword(email, otp, newPassword) { const r = await fetch(`${API_BASE_URL}/auth/reset-password`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ email: email.trim(), otp, new_password: newPassword }) }); const d = await parseResponse(r); if (!r.ok) throw new Error(d.detail || "Failed to reset password"); return d; }
export async function getProjects() { const r = await authenticatedFetch(`${API_BASE_URL}/projects`); const d = await parseResponse(r); if (!r.ok) throw new Error(d.detail || "Failed to load projects"); return d.projects || []; }
export async function getProject(id) { const r = await authenticatedFetch(`${API_BASE_URL}/projects/${id}`); const d = await parseResponse(r); if (!r.ok) throw new Error(d.detail || "Failed to load project"); return d; }
export async function deleteProject(id) { const r = await authenticatedFetch(`${API_BASE_URL}/projects/${id}`, { method: "DELETE" }); const d = await parseResponse(r); if (!r.ok) throw new Error(d.detail || "Failed to delete project"); return d; }
export async function uploadProject(file) { if (!isAuthenticated()) { logoutUser(); throw new Error("Please login before uploading a project."); } const f = new FormData(); f.append("file", file); const r = await authenticatedFetch(`${API_BASE_URL}/projects/upload`, { method: "POST", body: f }); const d = await parseResponse(r); if (!r.ok) throw new Error(d.detail || "Failed to upload project"); return d; }
