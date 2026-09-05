const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

export async function askAIArchitect(projectId, question, history = [], focus = null) {
  const token = localStorage.getItem("access_token");
  if (!token) throw new Error("Please login before using AI Architect.");

  const response = await fetch(`${API_BASE_URL}/projects/${projectId}/ai-architect`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ question, history, focus: focus ? {
      kind: focus.kind,
      target: focus.target,
      title: focus.title,
      smell_type: focus.smellType || "",
    } : null }),
  });

  const data = await response.json().catch(() => ({}));
  if (response.status === 401) {
    window.dispatchEvent(new Event("forgeiq:logout"));
    throw new Error("Your session has expired. Please login again.");
  }
  if (response.status === 409) throw new Error("This project does not have a saved analysis snapshot yet. Re-analyze the project first.");
  if (response.status === 503) throw new Error("AI Architect is not configured on the backend. Check the Gemini environment settings.");
  if (response.status === 502) throw new Error(data.detail || "Gemini could not process the request. Check the API key, model, or quota.");
  if (!response.ok) throw new Error(data.detail || "AI Architect request failed.");
  return data;
}
