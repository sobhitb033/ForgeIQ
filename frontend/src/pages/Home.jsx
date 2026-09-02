import { uploadProject } from "../services/api";
import { useState } from "react";
import AnalysisDashboard from "../components/AnalysisDashboard";

function Home() {
    const [selectedFile, setSelectedFile] = useState(null);
    const [analysisResult, setAnalysisResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleFileChange = (e) => {
        const file = e.target.files[0];

        if (!file) return;

        if (!file.name.endsWith(".zip")) {
            setError("Please select a ZIP file.");
            setSelectedFile(null);
            return;
        }

        setSelectedFile(file);
        setError("");
        setAnalysisResult(null);
    };

    const handleAnalyze = async () => {
        if (!selectedFile) {
            setError("Please select a ZIP file first.");
            return;
        }

        try {
            setLoading(true);
            setError("");
            setAnalysisResult(null);

            const data = await uploadProject(selectedFile);

            console.log("Analysis Result:", data);

            setAnalysisResult(data);

        } catch (err) {
            console.error(err);

            setError(
                err.message ||
                "Something went wrong while analyzing the project."
            );

        } finally {
            setLoading(false);
        }
    };

    return (
        <main className="home">
            {/* HERO */}

            <section className="hero">
                <div className="hero-content">
                    <div className="hero-badge">
                        AI-POWERED CODE ANALYSIS
                    </div>

                    <h1>
                        Understand your project.
                        <br />
                        <span>Improve your code.</span>
                    </h1>

                    <p>
                        Upload your project and let ForgeIQ analyze its
                        structure, architecture, dependencies, and code quality.
                    </p>
                </div>
            </section>

            {/* UPLOAD */}

            <section className="upload-section">
                <div className="upload-box">
                    <div className="upload-icon">
                        ↑
                    </div>

                    <h2>Upload your project</h2>

                    <p>
                        Drag and drop a ZIP file here, or click to browse.
                    </p>

                    <div className="file-actions">
                        <label className="file-button">
                            Choose file

                            <input
                                type="file"
                                accept=".zip"
                                onChange={handleFileChange}
                            />
                        </label>

                        <span className="file-name">
                            {selectedFile
                                ? selectedFile.name
                                : "No file selected"}
                        </span>
                    </div>

                    {error && (
                        <p className="error-message">
                            {error}
                        </p>
                    )}

                    <button
                        className="analyze-button"
                        onClick={handleAnalyze}
                        disabled={!selectedFile || loading}
                    >
                        {loading
                            ? "Analyzing Project..."
                            : "Analyze Project"}
                    </button>
                </div>
            </section>

            {/* LOADING */}

            {loading && (
                <div className="loading-container">
                    <div className="loader"></div>

                    <h3>Analyzing your project...</h3>

                    <p>
                        Inspecting files, architecture, dependencies,
                        and code quality.
                    </p>
                </div>
            )}

            {/* RESULTS */}

            {analysisResult && !loading && (
                <AnalysisDashboard
                    data={analysisResult}
                />
            )}
        </main>
    );
}

export default Home;