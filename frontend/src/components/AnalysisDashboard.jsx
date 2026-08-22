function AnalysisDashboard({ data }) {
    /* ============================= */
    /* SAFE DATA EXTRACTION */
    /* ============================= */

    const summary = data?.summary || {};

    const graphAnalysis =
        data?.graph_analysis || {};

    const architecture =
        data?.architecture || {};

    const projectHealth =
        data?.project_health || {};

    const recommendations =
        data?.recommendations || [];


    /* ============================= */
    /* ARCHITECTURE */
    /* ============================= */

    const coreModules =
        architecture?.core_modules || [];


    /* ============================= */
    /* DEPENDENCY ANALYSIS */
    /* ============================= */

    const mostConnectedModule =
        graphAnalysis?.most_connected_module ||
        graphAnalysis?.most_connected ||
        "N/A";


    const maximumDependencies =
        graphAnalysis?.max_dependencies ??
        graphAnalysis?.maximum_dependencies ??
        0;


    const circularDependencies =
        Array.isArray(
            graphAnalysis?.circular_dependencies
        )
            ? graphAnalysis.circular_dependencies.length
            : graphAnalysis?.circular_dependency_count ??
            graphAnalysis?.cycles?.length ??
            0;


    /* ============================= */
    /* PROJECT HEALTH */
    /* ============================= */

    const healthScore =
        projectHealth?.score ??
        data?.health_score ??
        0;


    const healthStatus =
        projectHealth?.status ??
        data?.health_status ??
        "Unknown";


    /* ============================= */
    /* HELPER FUNCTION */
    /* ============================= */

    const formatModuleName = (module) => {

        if (!module) {
            return "Unknown Module";
        }

        return String(module);
    };


    return (

        <section className="dashboard">


            {/* ============================= */}
            {/* PROJECT ANALYSIS HEADER */}
            {/* ============================= */}

            <div className="dashboard-header">

                <div>

                    <span className="section-tag">
                        ANALYSIS COMPLETE
                    </span>

                    <h2>
                        Project Analysis
                    </h2>

                    <p>
                        Here's what ForgeIQ discovered about your project.
                    </p>

                </div>

            </div>


            {/* ============================= */}
            {/* PROJECT HEALTH */}
            {/* ============================= */}

            <section className="health-card">

                <div className="health-info">

                    <span className="section-tag">
                        PROJECT HEALTH
                    </span>

                    <h3>
                        {healthStatus}
                    </h3>

                    <p>
                        Based on code structure,
                        dependencies, architecture,
                        and project quality.
                    </p>

                </div>


                <div className="health-score">

                    <span className="score-number">
                        {Number(healthScore).toFixed(2)}
                    </span>

                    <span className="score-total">
                        / 100
                    </span>

                </div>

            </section>


            {/* ============================= */}
            {/* PROJECT OVERVIEW */}
            {/* ============================= */}

            <section className="dashboard-section">

                <div className="section-heading">

                    <span className="section-tag">
                        PROJECT
                    </span>

                    <h3>
                        Project Overview
                    </h3>

                </div>


                <div className="stats-grid">

                    <StatCard
                        title="Total Files"
                        value={summary?.total_files ?? 0}
                    />

                    <StatCard
                        title="Total Lines"
                        value={summary?.total_lines ?? 0}
                    />

                    <StatCard
                        title="Code Lines"
                        value={summary?.code_lines ?? 0}
                    />

                    <StatCard
                        title="Classes"
                        value={summary?.total_classes ?? 0}
                    />

                    <StatCard
                        title="Functions"
                        value={summary?.total_functions ?? 0}
                    />

                    <StatCard
                        title="Methods"
                        value={summary?.total_methods ?? 0}
                    />

                </div>

            </section>


            {/* ============================= */}
            {/* ARCHITECTURE */}
            {/* ============================= */}

            <section className="dashboard-section">

                <div className="section-heading">

                    <span className="section-tag">
                        ARCHITECTURE
                    </span>

                    <h3>
                        Architecture
                    </h3>

                    <p>
                        {
                            architecture?.architecture_type ||
                            architecture?.type ||
                            "Project architecture analysis"
                        }
                    </p>

                </div>


                <h4 className="sub-heading">
                    Core Modules
                </h4>


                {
                    coreModules.length > 0
                        ? (

                            <div className="modules-grid">

                                {
                                    coreModules.map(
                                        (module, index) => (

                                            <div
                                                className="module-card"
                                                key={
                                                    module?.module ||
                                                    index
                                                }
                                            >

                                                <h4
                                                    className="module-name"
                                                    title={
                                                        formatModuleName(
                                                            module?.module
                                                        )
                                                    }
                                                >

                                                    {
                                                        formatModuleName(
                                                            module?.module
                                                        )
                                                    }

                                                </h4>


                                                <div className="module-row">

                                                    <span>
                                                        Fan In
                                                    </span>

                                                    <strong>
                                                        {
                                                            module?.fan_in ??
                                                            0
                                                        }
                                                    </strong>

                                                </div>


                                                <div className="module-row">

                                                    <span>
                                                        Fan Out
                                                    </span>

                                                    <strong>
                                                        {
                                                            module?.fan_out ??
                                                            0
                                                        }
                                                    </strong>

                                                </div>


                                                <div className="module-row">

                                                    <span>
                                                        Importance
                                                    </span>

                                                    <strong>
                                                        {
                                                            module?.importance_score ??
                                                            0
                                                        }
                                                    </strong>

                                                </div>

                                            </div>

                                        )
                                    )
                                }

                            </div>

                        )

                        : (

                            <div className="empty-card">

                                No core modules detected.

                            </div>

                        )
                }

            </section>


            {/* ============================= */}
            {/* DEPENDENCY ANALYSIS */}
            {/* ============================= */}

            <section className="dashboard-section">

                <div className="section-heading">

                    <span className="section-tag">
                        DEPENDENCIES
                    </span>

                    <h3>
                        Dependency Analysis
                    </h3>

                </div>


                <div className="dependency-grid">

                    <StatCard
                        title="Most Connected Module"
                        value={formatModuleName(
                            mostConnectedModule
                        )}
                        className="module-stat-card"
                    />


                    <StatCard
                        title="Maximum Dependencies"
                        value={maximumDependencies}
                    />


                    <StatCard
                        title="Circular Dependencies"
                        value={circularDependencies}
                        warning={
                            Number(
                                circularDependencies
                            ) > 0
                        }
                    />

                </div>

            </section>


            {/* ============================= */}
            {/* RECOMMENDATIONS */}
            {/* ============================= */}

            <section className="dashboard-section">

                <div className="section-heading">

                    <span className="section-tag">
                        INSIGHTS
                    </span>

                    <h3>
                        Recommendations
                    </h3>

                </div>


                {
                    recommendations.length > 0

                        ? (

                            <div className="recommendations-list">

                                {
                                    recommendations.map(
                                        (
                                            recommendation,
                                            index
                                        ) => (

                                            <div
                                                className="recommendation-card"
                                                key={index}
                                            >

                                                <div className="recommendation-number">

                                                    {index + 1}

                                                </div>


                                                <div className="recommendation-content">

                                                    <span
                                                        className={
                                                            `priority ${recommendation?.priority
                                                                ?.toLowerCase() ||
                                                            "low"
                                                            }`
                                                        }
                                                    >

                                                        {
                                                            recommendation?.priority ||
                                                            "Low"
                                                        }

                                                    </span>


                                                    <h4>

                                                        {
                                                            recommendation?.title ||
                                                            "Recommendation"
                                                        }

                                                    </h4>


                                                    {
                                                        recommendation?.message && (

                                                            <p className="recommendation-message">

                                                                {
                                                                    recommendation.message
                                                                }

                                                            </p>

                                                        )
                                                    }


                                                    {
                                                        recommendation?.recommendation && (

                                                            <p className="recommendation-text">

                                                                {
                                                                    recommendation.recommendation
                                                                }

                                                            </p>

                                                        )
                                                    }

                                                </div>

                                            </div>

                                        )
                                    )
                                }

                            </div>

                        )

                        : (

                            <div className="empty-card">

                                No recommendations generated.

                            </div>

                        )
                }

            </section>

        </section>

    );

}


/* ================================= */
/* REUSABLE STAT CARD */
/* ================================= */

function StatCard({
    title,
    value,
    warning = false,
    className = "",
}) {

    const isModuleName =
        className.includes("module-stat-card");


    return (

        <div
            className={
                `stat-card ${warning
                    ? "warning-card"
                    : ""
                } ${className}`
            }
        >

            <span className="stat-title">

                {title}

            </span>


            <strong
                className={
                    `stat-value ${isModuleName
                        ? "module-name"
                        : ""
                    }`
                }
                title={
                    typeof value === "string"
                        ? value
                        : ""
                }
            >

                {value}

            </strong>

        </div>

    );

}


export default AnalysisDashboard;