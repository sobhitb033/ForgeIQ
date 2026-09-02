const API_BASE_URL =
    import.meta.env.VITE_API_BASE_URL ||
    "http://127.0.0.1:8000";


export async function registerUser(userData) {

    const response = await fetch(
        `${API_BASE_URL}/auth/register`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
            },

            body: JSON.stringify(userData),
        }
    );

    const data = await response.json();

    if (!response.ok) {

        throw new Error(
            data.detail || "Registration failed"
        );
    }

    return data;
}


export async function loginUser(
    email,
    password
) {

    const formData = new URLSearchParams();

    formData.append(
        "username",
        email
    );

    formData.append(
        "password",
        password
    );


    const response = await fetch(
        `${API_BASE_URL}/auth/login`,
        {
            method: "POST",

            headers: {
                "Content-Type":
                    "application/x-www-form-urlencoded",
            },

            body: formData.toString(),
        }
    );


    const data = await response.json();

    if (!response.ok) {

        throw new Error(
            data.detail || "Login failed"
        );
    }


    localStorage.setItem(
        "access_token",
        data.access_token
    );

    return data;
}

export async function googleLogin(credential) {

    const response = await fetch(
        `${API_BASE_URL}/auth/google`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
            },

            body: JSON.stringify({
                credential: credential,
            }),
        }
    );


    const data = await response.json();


    if (!response.ok) {

        throw new Error(
            data.detail ||
            "Google login failed"
        );
    }


    localStorage.setItem(
        "access_token",
        data.access_token
    );


    return data;
}

export async function forgotPassword(email) {

    const response = await fetch(
        `${API_BASE_URL}/auth/forgot-password`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
            },

            body: JSON.stringify({
                email: email.trim(),
            }),
        }
    );


    const data = await response.json();

    if (!response.ok) {

        throw new Error(
            data.detail ||
            "Failed to send password reset OTP"
        );
    }

    return data;
}


export async function verifyOTP(
    email,
    otp
) {

    const response = await fetch(
        `${API_BASE_URL}/auth/verify-otp`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
            },

            body: JSON.stringify({
                email: email.trim(),
                otp: otp,
            }),
        }
    );


    const data = await response.json();

    if (!response.ok) {

        throw new Error(
            data.detail ||
            "Invalid or expired OTP"
        );
    }

    return data;
}


export async function resetPassword(
    email,
    otp,
    newPassword
) {

    const response = await fetch(
        `${API_BASE_URL}/auth/reset-password`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
            },

            body: JSON.stringify({
                email: email.trim(),
                otp: otp,
                new_password: newPassword,
            }),
        }
    );


    const data = await response.json();

    if (!response.ok) {

        throw new Error(
            data.detail ||
            "Failed to reset password"
        );
    }

    return data;
}

export async function uploadProject(file) {

    const token =
        localStorage.getItem(
            "access_token"
        );


    if (!token) {

        throw new Error(
            "Please login before uploading a project."
        );
    }


    const formData = new FormData();

    formData.append(
        "file",
        file
    );


    const response = await fetch(
        `${API_BASE_URL}/projects/upload`,
        {
            method: "POST",

            headers: {
                Authorization:
                    `Bearer ${token}`,
            },

            body: formData,
        }
    );


    const data = await response.json();

    if (!response.ok) {

        throw new Error(
            data.detail ||
            "Failed to upload project"
        );
    }

    return data;
}


export function logoutUser() {

    localStorage.removeItem(
        "access_token"
    );
}


export function isAuthenticated() {

    return !!localStorage.getItem(
        "access_token"
    );
}