class RecommendationEngine:

    @staticmethod
    def generate(
        analysis,
        graph_analysis,
        project_health,
        architecture
    ):

        recommendations = []

        # Circular dependency recommendations
        recommendations.extend(
            RecommendationEngine.circular_dependency_recommendations(
                graph_analysis
            )
        )

        # Code smell recommendations
        recommendations.extend(
            RecommendationEngine.code_smell_recommendations(
                analysis
            )
        )

        # Engineering priority recommendations
        recommendations.extend(
            RecommendationEngine.priority_recommendations(
                analysis
            )
        )

        # Architecture recommendations
        recommendations.extend(
            RecommendationEngine.architecture_recommendations(
                architecture
            )
        )

        # Project health recommendations
        recommendations.extend(
            RecommendationEngine.project_health_recommendations(
                project_health
            )
        )

        # Sort recommendations by priority
        recommendations = (
            RecommendationEngine.sort_recommendations(
                recommendations
            )
        )

        return recommendations

    @staticmethod
    def circular_dependency_recommendations(
        graph_analysis
    ):

        recommendations = []

        circular_dependencies = (
            graph_analysis.get(
                "circular_dependencies",
                []
            )
        )

        for cycle in circular_dependencies:

            modules = " → ".join(cycle)

            recommendations.append(
                {
                    "category": "Dependency",
                    "priority": "High",
                    "title": "Break Circular Dependency",
                    "message": (
                        f"Circular dependency detected: "
                        f"{modules}."
                    ),
                    "recommendation": (
                        "Restructure the dependencies between "
                        "these modules. Consider extracting "
                        "shared functionality into a separate "
                        "module or using dependency injection."
                    )
                }
            )

        return recommendations

    @staticmethod
    def code_smell_recommendations(
        analysis
    ):

        recommendations = []

        for file_data in analysis:

            file_path = file_data.get(
                "file",
                "Unknown"
            )

            code_smells = file_data.get(
                "code_smells",
                []
            )

            for smell in code_smells:

                smell_type = smell.get(
                    "type",
                    "Code Smell"
                )

                severity = smell.get(
                    "severity",
                    "Low"
                )

                location = smell.get(
                    "location",
                    "Unknown"
                )

                if smell_type == "Missing Docstring":

                    recommendation = (
                        "Add a clear docstring explaining "
                        "the purpose, parameters, and return "
                        "value where applicable."
                    )

                else:

                    recommendation = (
                        "Review this code smell and refactor "
                        "the affected code to improve "
                        "maintainability."
                    )

                recommendations.append(
                    {
                        "category": "Code Quality",
                        "priority": severity,
                        "title": smell_type,
                        "file": file_path,
                        "location": location,
                        "message": smell.get(
                            "message",
                            f"{smell_type} detected."
                        ),
                        "recommendation": recommendation
                    }
                )

        return recommendations

    @staticmethod
    def priority_recommendations(
        analysis
    ):

        recommendations = []

        for file_data in analysis:

            file_path = file_data.get(
                "file",
                "Unknown"
            )

            priority_data = file_data.get(
                "engineering_priority",
                {}
            )

            priority = priority_data.get(
                "priority",
                "Low"
            )

            score = priority_data.get(
                "score",
                0
            )

            if priority in ["High", "Critical"]:

                recommendations.append(
                    {
                        "category": "Engineering Priority",
                        "priority": priority,
                        "title": (
                            "High Priority File Requires "
                            "Attention"
                        ),
                        "file": file_path,
                        "message": (
                            f"This file has an engineering "
                            f"priority score of {score}."
                        ),
                        "recommendation": (
                            "Review this file first. Address "
                            "the factors contributing to its "
                            "engineering priority score."
                        )
                    }
                )

        return recommendations

    @staticmethod
    def architecture_recommendations(
        architecture
    ):

        recommendations = []

        issues = architecture.get(
            "issues",
            []
        )

        for issue in issues:

            issue_type = issue.get(
                "type",
                "Architecture Issue"
            )

            severity = issue.get(
                "severity",
                "Medium"
            )

            module = issue.get(
                "module",
                "Unknown"
            )

            if issue_type == "High Coupling":

                recommendation = (
                    "Reduce the number of direct dependencies "
                    "by separating responsibilities or "
                    "introducing abstraction layers."
                )

            elif issue_type == "High Dependency":

                recommendation = (
                    "Review this highly depended-on module "
                    "carefully. Changes to it may have a "
                    "large impact across the project."
                )

            elif issue_type == "Orphan Module":

                recommendation = (
                    "Check whether this module is unused. "
                    "Remove it if unnecessary or integrate "
                    "it properly into the project."
                )

            else:

                recommendation = (
                    "Review the architectural issue and "
                    "refactor the affected module."
                )

            recommendations.append(
                {
                    "category": "Architecture",
                    "priority": severity,
                    "title": issue_type,
                    "module": module,
                    "message": issue.get(
                        "message",
                        f"{issue_type} detected."
                    ),
                    "recommendation": recommendation
                }
            )

        return recommendations

    @staticmethod
    def project_health_recommendations(
        project_health
    ):

        recommendations = []

        score = project_health.get(
            "score",
            100
        )

        status = project_health.get(
            "status",
            "Excellent"
        )

        if score < 50:

            recommendations.append(
                {
                    "category": "Project Health",
                    "priority": "Critical",
                    "title": "Poor Project Health",
                    "message": (
                        f"The project health score is "
                        f"{score} ({status})."
                    ),
                    "recommendation": (
                        "Prioritize fixing critical "
                        "architectural issues, code smells, "
                        "and high-priority files."
                    )
                }
            )

        elif score < 70:

            recommendations.append(
                {
                    "category": "Project Health",
                    "priority": "High",
                    "title": "Project Health Needs Improvement",
                    "message": (
                        f"The project health score is "
                        f"{score} ({status})."
                    ),
                    "recommendation": (
                        "Address the most important "
                        "recommendations, especially "
                        "dependency and architectural issues."
                    )
                }
            )

        elif score < 85:

            recommendations.append(
                {
                    "category": "Project Health",
                    "priority": "Medium",
                    "title": "Project Health Can Be Improved",
                    "message": (
                        f"The project health score is "
                        f"{score} ({status})."
                    ),
                    "recommendation": (
                        "Continue improving maintainability "
                        "and resolving detected code quality "
                        "issues."
                    )
                }
            )

        return recommendations

    @staticmethod
    def sort_recommendations(
        recommendations
    ):

        priority_order = {
            "Critical": 1,
            "High": 2,
            "Medium": 3,
            "Low": 4
        }

        recommendations.sort(
            key=lambda item: priority_order.get(
                item.get("priority", "Low"),
                4
            )
        )

        return recommendations