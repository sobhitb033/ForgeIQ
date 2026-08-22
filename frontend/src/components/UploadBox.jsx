import { useState } from "react";
import { uploadProject } from "../services/api";

function UploadBox({ setAnalysisResult }) {
    const [selectedFile, setSelectedFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleFileChange = (event) => {
        const file = event.target.files[0];

        if (file) {
            setSelectedFile(file);
            setError("");
        }
    };

    const handleAnalyze = async () => {
        if (!selectedFile) {
            setError("Please select a ZIP file first.");
            return;
        }

        try {
            setLoading(true);
            setError("");

            const result = await uploadProject(selectedFile);

            console.log("Analysis result:", result);

            // Send result to Home.jsx
            setAnalysisResult(result);

        } catch (error) {
            console.error(error);
            setError(error.message || "Something went wrong.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <section className="upload-section">
            <div className="upload-container">

                <h1>Analyze Your Project</h1>

                <p>
                    Upload your project files and let ForgeIQ analyze your code,
                    architecture, dependencies, and project health.
                </p>

                <div className="upload-box">

                    <div className="upload-icon">↑</div>

                    <h2>Upload your project</h2>

                    <p>
                        Drag and drop a ZIP file here, or click to browse.
                    </p>

                    <input
                        type="file"
                        accept=".zip"
                        onChange={handleFileChange}
                    />

                    {selectedFile && (
                        <p className="selected-file">
                            {selectedFile.name}
                        </p>
                    )}

                    <button
                        onClick={handleAnalyze}
                        disabled={loading}
                    >
                        {loading
                            ? "Analyzing..."
                            : "Analyze Project"
                        }
                    </button>

                    {error && (
                        <p className="error-message">
                            {error}
                        </p>
                    )}

                </div>
            </div>
        </section>
    );
}

export default UploadBox;