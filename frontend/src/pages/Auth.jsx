import { useEffect, useState } from "react";

import {
    registerUser,
    loginUser,
    googleLogin,
    forgotPassword,
    verifyOTP,
    resetPassword,
} from "../services/api";


function Auth({ onLogin }) {


    const [authMode, setAuthMode] = useState("login");

    const [email, setEmail] = useState("");
    const [fullName, setFullName] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");

    const [showPassword, setShowPassword] = useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = useState(false);
    const [otp, setOtp] = useState("");

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");

    const googleClientId =
        import.meta.env.VITE_GOOGLE_CLIENT_ID;

    useEffect(() => {

        const initializeGoogle = () => {

            if (!window.google) {
                return;
            }


            window.google.accounts.id.initialize({

                client_id: googleClientId,

                callback: async (response) => {

                    try {

                        setLoading(true);
                        setError("");
                        setSuccess("");


                        await googleLogin(
                            response.credential
                        );


                        onLogin();

                    } catch (err) {

                        console.error(err);

                        setError(
                            err.message ||
                            "Google login failed. Please try again."
                        );

                    } finally {

                        setLoading(false);
                    }

                },

            });


            window.google.accounts.id.renderButton(

                document.getElementById(
                    "google-signin-button"
                ),

                {
                    theme: "outline",
                    size: "large",
                    width: 300,
                    text: "continue_with",
                    shape: "rectangular",
                }

            );

        };


        if (
            document.getElementById(
                "google-signin-script"
            )
        ) {

            initializeGoogle();

            return;
        }


        const script =
            document.createElement("script");

        script.id = "google-signin-script";

        script.src =
            "https://accounts.google.com/gsi/client";

        script.async = true;
        script.defer = true;

        script.onload =
            initializeGoogle;

        document.body.appendChild(script);


        return () => {

            /*
             * Google owns the script.
             * We don't remove it because React can
             * remount this component during development.
             */

        };

    }, [googleClientId, onLogin]);


    /*
     * Reset all form fields.
     */
    const clearFields = () => {

        setEmail("");
        setFullName("");
        setPassword("");
        setConfirmPassword("");
        setOtp("");

        setShowPassword(false);
        setShowConfirmPassword(false);

    };


    /*
     * Switch between Login and Register.
     */
    const switchMode = (mode) => {

        setAuthMode(mode);

        clearFields();

        setError("");
        setSuccess("");

    };


    /*
     * Go back to login from any password-reset step.
     */
    const goToLogin = () => {

        setAuthMode("login");

        setPassword("");
        setConfirmPassword("");
        setOtp("");

        setError("");
        setSuccess("");

    };


    /*
     * Normal Login / Registration
     */
    const handleAuthSubmit = async (event) => {

        event.preventDefault();

        setError("");
        setSuccess("");


        if (
            authMode === "register" &&
            password !== confirmPassword
        ) {

            setError("Passwords do not match.");

            return;
        }


        try {

            setLoading(true);


            if (authMode === "login") {

                await loginUser(
                    email.trim(),
                    password
                );

                onLogin();

            } else {

                await registerUser({
                    email: email.trim(),
                    password: password,
                    full_name: fullName.trim(),
                });


                setSuccess(
                    "Account created successfully. Logging you in..."
                );


                await loginUser(
                    email.trim(),
                    password
                );


                onLogin();
            }

        } catch (err) {

            console.error(err);

            setError(
                err.message ||
                "Authentication failed. Please try again."
            );

        } finally {

            setLoading(false);
        }

    };


    /*
     * Request OTP
     */
    const handleForgotPassword = async (event) => {

        event.preventDefault();

        setError("");
        setSuccess("");


        try {

            setLoading(true);


            await forgotPassword(
                email.trim()
            );


            /*
             * We move to OTP screen regardless of whether
             * the email exists.
             *
             * This matches the backend's security-friendly
             * generic response.
             */
            setAuthMode("otp");

            setSuccess(
                "If an account exists with this email, an OTP has been sent."
            );

        } catch (err) {

            console.error(err);

            setError(
                err.message ||
                "Unable to send OTP. Please try again."
            );

        } finally {

            setLoading(false);
        }

    };


    /*
     * Verify OTP
     */
    const handleVerifyOTP = async (event) => {

        event.preventDefault();

        setError("");
        setSuccess("");


        if (otp.length !== 6) {

            setError("Please enter the 6-digit OTP.");

            return;
        }


        try {

            setLoading(true);


            await verifyOTP(
                email.trim(),
                otp
            );


            setAuthMode("reset");

            setSuccess(
                "OTP verified successfully."
            );

        } catch (err) {

            console.error(err);

            setError(
                err.message ||
                "Invalid or expired OTP."
            );

        } finally {

            setLoading(false);
        }

    };


    /*
     * Reset Password
     */
    const handleResetPassword = async (event) => {

        event.preventDefault();

        setError("");
        setSuccess("");


        if (password.length < 8) {

            setError(
                "Password must be at least 8 characters."
            );

            return;
        }


        if (password !== confirmPassword) {

            setError(
                "Passwords do not match."
            );

            return;
        }


        try {

            setLoading(true);


            await resetPassword(
                email.trim(),
                otp,
                password
            );


            setSuccess(
                "Password reset successfully. You can now login."
            );


            /*
             * Clear password fields before returning
             * to the login screen.
             */
            setPassword("");
            setConfirmPassword("");
            setOtp("");


            setTimeout(() => {

                setAuthMode("login");

                setError("");
                setSuccess("");

            }, 1500);

        } catch (err) {

            console.error(err);

            setError(
                err.message ||
                "Failed to reset password. Please try again."
            );

        } finally {

            setLoading(false);
        }

    };


    /*
     * Common error/success messages.
     */
    const messages = (
        <>
            {error && (
                <p className="login-error">
                    {error}
                </p>
            )}

            {success && (
                <p className="login-success">
                    {success}
                </p>
            )}
        </>
    );


    return (

        <main className="login-page">

            <div className="login-card">

                {/* BRAND */}

                <div className="login-brand">

                    <span className="login-logo">
                        ⚡
                    </span>

                    <h1>
                        ForgeIQ
                    </h1>

                </div>


                {authMode === "login" && (

                    <>

                        <h2>
                            Welcome back
                        </h2>

                        <p>
                            Login to analyze and manage your projects.
                        </p>


                        <form onSubmit={handleAuthSubmit}>

                            <label htmlFor="login-email">
                                Email
                            </label>

                            <input
                                id="login-email"
                                type="email"
                                placeholder="you@example.com"
                                value={email}
                                onChange={(event) =>
                                    setEmail(event.target.value)
                                }
                                autoComplete="email"
                                required
                            />


                            <label htmlFor="login-password">
                                Password
                            </label>

                            <div className="password-input-wrapper">

                                <input
                                    id="login-password"
                                    type={
                                        showPassword
                                            ? "text"
                                            : "password"
                                    }
                                    placeholder="Enter your password"
                                    value={password}
                                    onChange={(event) =>
                                        setPassword(event.target.value)
                                    }
                                    autoComplete="current-password"
                                    minLength={8}
                                    required
                                />

                                <button
                                    type="button"
                                    className="password-toggle"
                                    onClick={() =>
                                        setShowPassword(!showPassword)
                                    }
                                    aria-label={
                                        showPassword
                                            ? "Hide password"
                                            : "Show password"
                                    }
                                    title={
                                        showPassword
                                            ? "Hide password"
                                            : "Show password"
                                    }
                                >
                                    {showPassword ? "◉" : "◌"}
                                </button>

                            </div>


                            <div className="forgot-password-link">

                                <button
                                    type="button"
                                    onClick={() =>
                                        switchMode("forgot")
                                    }
                                >
                                    Forgot password?
                                </button>

                            </div>


                            {messages}


                            <button
                                type="submit"
                                disabled={loading}
                            >
                                {loading
                                    ? "Logging in..."
                                    : "Login"}
                            </button>

                        </form>

                        <div className="google-login-section">

                            <div className="google-divider">
                                <span>OR</span>
                            </div>

                            <div
                                id="google-signin-button"
                                className="google-signin-button"
                            ></div>

                        </div>

                        <div className="auth-switch">

                            <span>
                                Don't have an account?
                            </span>

                            <button
                                type="button"
                                onClick={() =>
                                    switchMode("register")
                                }
                            >
                                Create account
                            </button>

                        </div>

                    </>
                )}


                {authMode === "register" && (

                    <>

                        <h2>
                            Create your account
                        </h2>

                        <p>
                            Join ForgeIQ and start understanding your code.
                        </p>


                        <form onSubmit={handleAuthSubmit}>

                            <label htmlFor="register-full-name">
                                Full Name
                            </label>

                            <input
                                id="register-full-name"
                                type="text"
                                placeholder="Your full name"
                                value={fullName}
                                onChange={(event) =>
                                    setFullName(event.target.value)
                                }
                                autoComplete="name"
                                required
                            />


                            <label htmlFor="register-email">
                                Email
                            </label>

                            <input
                                id="register-email"
                                type="email"
                                placeholder="you@example.com"
                                value={email}
                                onChange={(event) =>
                                    setEmail(event.target.value)
                                }
                                autoComplete="email"
                                required
                            />


                            <label htmlFor="register-password">
                                Password
                            </label>

                            <div className="password-input-wrapper">

                                <input
                                    id="register-password"
                                    type={
                                        showPassword
                                            ? "text"
                                            : "password"
                                    }
                                    placeholder="Enter your password"
                                    value={password}
                                    onChange={(event) =>
                                        setPassword(event.target.value)
                                    }
                                    autoComplete="new-password"
                                    minLength={8}
                                    required
                                />

                                <button
                                    type="button"
                                    className="password-toggle"
                                    onClick={() =>
                                        setShowPassword(!showPassword)
                                    }
                                    aria-label={
                                        showPassword
                                            ? "Hide password"
                                            : "Show password"
                                    }
                                    title={
                                        showPassword
                                            ? "Hide password"
                                            : "Show password"
                                    }
                                >
                                    {showPassword ? "◉" : "◌"}
                                </button>

                            </div>


                            <label htmlFor="register-confirm-password">
                                Confirm Password
                            </label>

                            <div className="password-input-wrapper">

                                <input
                                    id="register-confirm-password"
                                    type={
                                        showConfirmPassword
                                            ? "text"
                                            : "password"
                                    }
                                    placeholder="Re-enter your password"
                                    value={confirmPassword}
                                    onChange={(event) =>
                                        setConfirmPassword(event.target.value)
                                    }
                                    autoComplete="new-password"
                                    minLength={8}
                                    required
                                />

                                <button
                                    type="button"
                                    className="password-toggle"
                                    onClick={() =>
                                        setShowConfirmPassword(
                                            !showConfirmPassword
                                        )
                                    }
                                    aria-label={
                                        showConfirmPassword
                                            ? "Hide password"
                                            : "Show password"
                                    }
                                    title={
                                        showConfirmPassword
                                            ? "Hide password"
                                            : "Show password"
                                    }
                                >
                                    {showConfirmPassword ? "◉" : "◌"}
                                </button>

                            </div>


                            {messages}


                            <button
                                type="submit"
                                disabled={loading}
                            >
                                {loading
                                    ? "Creating account..."
                                    : "Create Account"}
                            </button>

                        </form>


                        <div className="auth-switch">

                            <span>
                                Already have an account?
                            </span>

                            <button
                                type="button"
                                onClick={() =>
                                    switchMode("login")
                                }
                            >
                                Login
                            </button>

                        </div>

                    </>
                )}


                {authMode === "forgot" && (

                    <>

                        <h2>
                            Forgot your password?
                        </h2>

                        <p>
                            Enter your email and we'll send you a
                            6-digit OTP to reset your password.
                        </p>


                        <form onSubmit={handleForgotPassword}>

                            <label htmlFor="forgot-email">
                                Email
                            </label>

                            <input
                                id="forgot-email"
                                type="email"
                                placeholder="you@example.com"
                                value={email}
                                onChange={(event) =>
                                    setEmail(event.target.value)
                                }
                                autoComplete="email"
                                required
                            />


                            {messages}


                            <button
                                type="submit"
                                disabled={loading}
                            >
                                {loading
                                    ? "Sending OTP..."
                                    : "Send OTP"}
                            </button>

                        </form>


                        <div className="auth-switch">

                            <button
                                type="button"
                                onClick={goToLogin}
                            >
                                ← Back to Login
                            </button>

                        </div>

                    </>
                )}


                {authMode === "otp" && (

                    <>

                        <h2>
                            Verify OTP
                        </h2>

                        <p>
                            Enter the 6-digit OTP sent to
                            <br />
                            <strong>
                                {email}
                            </strong>
                        </p>


                        <form onSubmit={handleVerifyOTP}>

                            <label htmlFor="otp">
                                OTP
                            </label>

                            <input
                                id="otp"
                                type="text"
                                inputMode="numeric"
                                maxLength={6}
                                placeholder="000000"
                                value={otp}
                                onChange={(event) =>
                                    setOtp(
                                        event.target.value
                                            .replace(/\D/g, "")
                                    )
                                }
                                autoComplete="one-time-code"
                                required
                            />


                            {messages}


                            <button
                                type="submit"
                                disabled={
                                    loading ||
                                    otp.length !== 6
                                }
                            >
                                {loading
                                    ? "Verifying..."
                                    : "Verify OTP"}
                            </button>

                        </form>


                        <div className="auth-switch">

                            <button
                                type="button"
                                onClick={() =>
                                    switchMode("forgot")
                                }
                            >
                                ← Change email
                            </button>

                        </div>

                    </>
                )}


                {authMode === "reset" && (

                    <>

                        <h2>
                            Create a new password
                        </h2>

                        <p>
                            Your OTP has been verified.
                            Choose a new password for your account.
                        </p>


                        <form onSubmit={handleResetPassword}>

                            <label htmlFor="new-password">
                                New Password
                            </label>

                            <div className="password-input-wrapper">

                                <input
                                    id="new-password"
                                    type={
                                        showPassword
                                            ? "text"
                                            : "password"
                                    }
                                    placeholder="Enter new password"
                                    value={password}
                                    onChange={(event) =>
                                        setPassword(event.target.value)
                                    }
                                    autoComplete="new-password"
                                    minLength={8}
                                    required
                                />

                                <button
                                    type="button"
                                    className="password-toggle"
                                    onClick={() =>
                                        setShowPassword(!showPassword)
                                    }
                                    aria-label={
                                        showPassword
                                            ? "Hide password"
                                            : "Show password"
                                    }
                                    title={
                                        showPassword
                                            ? "Hide password"
                                            : "Show password"
                                    }
                                >
                                    {showPassword ? "◉" : "◌"}
                                </button>

                            </div>


                            <label htmlFor="new-confirm-password">
                                Confirm New Password
                            </label>

                            <div className="password-input-wrapper">

                                <input
                                    id="new-confirm-password"
                                    type={
                                        showConfirmPassword
                                            ? "text"
                                            : "password"
                                    }
                                    placeholder="Re-enter new password"
                                    value={confirmPassword}
                                    onChange={(event) =>
                                        setConfirmPassword(event.target.value)
                                    }
                                    autoComplete="new-password"
                                    minLength={8}
                                    required
                                />

                                <button
                                    type="button"
                                    className="password-toggle"
                                    onClick={() =>
                                        setShowConfirmPassword(
                                            !showConfirmPassword
                                        )
                                    }
                                    aria-label={
                                        showConfirmPassword
                                            ? "Hide password"
                                            : "Show password"
                                    }
                                    title={
                                        showConfirmPassword
                                            ? "Hide password"
                                            : "Show password"
                                    }
                                >
                                    {showConfirmPassword ? "◉" : "◌"}
                                </button>

                            </div>


                            {messages}


                            <button
                                type="submit"
                                disabled={loading}
                            >
                                {loading
                                    ? "Resetting password..."
                                    : "Reset Password"}
                            </button>

                        </form>


                        <div className="auth-switch">

                            <button
                                type="button"
                                onClick={goToLogin}
                            >
                                ← Back to Login
                            </button>

                        </div>

                    </>
                )}

            </div>

        </main>
    );
}


export default Auth;