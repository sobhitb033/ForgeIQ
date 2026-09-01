import { useState } from "react";

function FileAnalysis({ files }) {
    const [selectedFile, setSelectedFile] = useState(null);

    if (!files || files.length === 0) {
        return null;
    }

    return (
        <section className="file-analysis-section">

            <div className="section-label">
                FILE ANALYSIS
            </div>

            <h2 className="section-title">
                Source Code Analysis
            </h2>

            <p className="section-description">
                Explore detailed metrics, code quality issues,
                dependencies, and engineering priority for every file.
            </p>

            <div className="file-analysis-grid">

                {files.map((fileData, index) => {

                    const metrics =
                        fileData.metrics || {};

                    const priorityData =
                        fileData.engineering_priority || {};

                    const maintainability =
                        fileData.maintainability || {};

                    const codeSmells =
                        fileData.code_smells || [];

                    const dependencies =
                        fileData.dependencies || {};


                    // Determine maintainability display value
                    const maintainabilityValue =
                        maintainability.rating ??
                        maintainability.status ??
                        maintainability.level ??
                        maintainability.score ??
                        "N/A";

                    return (
                        <div
                            className={`file-card ${selectedFile === index ? "active" : ""
                                }`}
                            key={index}
                        >

                            {/* FILE HEADER */}

                            <div className="file-card-header">

                                <h3>
                                    {fileData.file}
                                </h3>

                                <span
                                    className={`priority-badge ${priorityData.priority
                                        ?.toLowerCase() || "low"
                                        }`}
                                >
                                    {priorityData.priority || "Low"}
                                </span>

                            </div>


                            {/* FILE STATS */}

                            <div className="file-stats">

                                <div className="file-stat">

                                    <span>
                                        Maintainability
                                    </span>

                                    <strong>
                                        {maintainabilityValue}
                                    </strong>

                                </div>


                                <div className="file-stat">

                                    <span>
                                        Code Smells
                                    </span>

                                    <strong>
                                        {codeSmells.length}
                                    </strong>

                                </div>


                                <div className="file-stat">

                                    <span>
                                        Dependencies
                                    </span>

                                    <strong>
                                        {
                                            dependencies.internal
                                                ?.length || 0
                                        }
                                    </strong>

                                </div>

                            </div>


                            {/* DETAILS BUTTON */}

                            <button
                                className="file-details-button"
                                onClick={() =>
                                    setSelectedFile(
                                        selectedFile === index
                                            ? null
                                            : index
                                    )
                                }
                            >
                                {selectedFile === index
                                    ? "Hide Details"
                                    : "View Details"}
                            </button>


                            {/* EXPANDED DETAILS */}

                            {selectedFile === index && (

                                <div className="file-details">

                                    {/* METRICS */}

                                    <h4>
                                        Metrics
                                    </h4>

                                    <div className="details-grid">

                                        <div>

                                            <span>
                                                Total Lines
                                            </span>

                                            <strong>
                                                {
                                                    metrics.total_lines ??
                                                    "N/A"
                                                }
                                            </strong>

                                        </div>


                                        <div>

                                            <span>
                                                Code Lines
                                            </span>

                                            <strong>
                                                {
                                                    metrics.code_lines ??
                                                    "N/A"
                                                }
                                            </strong>

                                        </div>


                                        <div>

                                            <span>
                                                Classes
                                            </span>

                                            <strong>
                                                {
                                                    metrics.classes ??
                                                    "N/A"
                                                }
                                            </strong>

                                        </div>


                                        <div>

                                            <span>
                                                Functions
                                            </span>

                                            <strong>
                                                {
                                                    metrics.functions ??
                                                    "N/A"
                                                }
                                            </strong>

                                        </div>

                                    </div>


                                    {/* MAINTAINABILITY DETAILS */}

                                    <h4>
                                        Maintainability
                                    </h4>

                                    <div className="details-grid">

                                        <div>

                                            <span>
                                                Rating
                                            </span>

                                            <strong>
                                                {
                                                    maintainability.rating ??
                                                    maintainability.status ??
                                                    maintainability.level ??
                                                    "N/A"
                                                }
                                            </strong>

                                        </div>


                                        <div>

                                            <span>
                                                Score
                                            </span>

                                            <strong>
                                                {
                                                    maintainability.index ??
                                                    "N/A"
                                                }
                                            </strong>

                                        </div>

                                    </div>


                                    {/* CODE SMELLS */}

                                    <h4>
                                        Code Smells
                                    </h4>

                                    {codeSmells.length > 0 ? (

                                        <div className="smell-list">

                                            {codeSmells.map(
                                                (
                                                    smell,
                                                    smellIndex
                                                ) => (

                                                    <div
                                                        className="smell-item"
                                                        key={smellIndex}
                                                    >

                                                        <strong>
                                                            {
                                                                smell.type ||
                                                                "Code Smell"
                                                            }
                                                        </strong>

                                                        <p>
                                                            {
                                                                smell.message ||
                                                                "No description available."
                                                            }
                                                        </p>

                                                    </div>

                                                )
                                            )}

                                        </div>

                                    ) : (

                                        <p className="empty-state">

                                            No code smells detected.

                                        </p>

                                    )}


                                    {/* INTERNAL DEPENDENCIES */}

                                    <h4>
                                        Internal Dependencies
                                    </h4>

                                    {
                                        dependencies.internal
                                            ?.length > 0
                                            ? (

                                                <div className="dependency-list">

                                                    {
                                                        dependencies.internal.map(
                                                            (
                                                                dependency,
                                                                dependencyIndex
                                                            ) => (

                                                                <span
                                                                    className="dependency-tag"
                                                                    key={
                                                                        dependencyIndex
                                                                    }
                                                                >

                                                                    {
                                                                        dependency
                                                                    }

                                                                </span>

                                                            )
                                                        )
                                                    }

                                                </div>

                                            )

                                            : (

                                                <p className="empty-state">

                                                    No internal dependencies.

                                                </p>

                                            )
                                    }

                                </div>

                            )}

                        </div>
                    );
                })}

            </div>

        </section>
    );
}

export default FileAnalysis;