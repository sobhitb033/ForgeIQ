const API_BASE_URL = "http://127.0.0.1:8000";

export async function uploadProject(file) {
    const formData = new FormData();

    formData.append("file", file);

    const response = await fetch(
        `${API_BASE_URL}/projects/upload`,
        {
            method: "POST",
            body: formData,
        }
    );

    if (!response.ok) {
        const errorData = await response.json();

        throw new Error(
            errorData.detail || "Failed to upload project"
        );
    }

    return response.json();
}