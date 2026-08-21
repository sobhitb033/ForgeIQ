class ProjectReportGenerator:

    @staticmethod
    def generate(
        summary,
        project_health,
        architecture,
        graph_analysis,
        recommendations,
        analysis,
    ):

        strengths = (
            ProjectReportGenerator.generate_strengths(
                summary,
                project_health,
                analysis,
            )
        )

        critical_issues = (
            ProjectReportGenerator.generate_critical_issues(
                graph_analysis,
                architecture,
                recommendations,
            )
        )

        architecture_summary = (
            ProjectReportGenerator.generate_architecture_summary(
                architecture
            )
        )

        recommended_actions = (
            ProjectReportGenerator.generate_recommended_actions(
                recommendations
            )
        )

        file_summary = (
            ProjectReportGenerator.generate_file_summary(
                analysis
            )
        )

        return {
            "overview": {
                "health_score": project_health["score"],
                "health_status": project_health["status"],
                "architecture": architecture[
                    "architecture_type"
                ],
                "total_files": summary["total_files"],
                "total_lines": summary["total_lines"],
                "total_code_lines": summary["code_lines"],
                "total_classes": summary["total_classes"],
                "total_functions": summary[
                    "total_functions"
                ],
            },

            "strengths": strengths,

            "critical_issues": critical_issues,

            "architecture_summary": architecture_summary,

            "recommended_actions": recommended_actions,

            "file_summary": file_summary,
        }

    @staticmethod
    def generate_strengths(
        summary,
        project_health,
        analysis,
    ):

        strengths = []

        average_maintainability = (
            project_health["factors"][
                "average_maintainability"
            ]
        )

        if average_maintainability >= 85:

            strengths.append(
                {
                    "title": "High Maintainability",
                    "message": (
                        "The project has a strong average "
                        "maintainability score, making the code "
                        "relatively easy to understand and modify."
                    )
                }
            )

        low_complexity_files = 0

        for file_data in analysis:

            functions = (
                file_data["ast"]["functions"]
            )

            classes = (
                file_data["ast"]["classes"]
            )

            all_complexities = []

            for function in functions:

                all_complexities.append(
                    function.get(
                        "cyclomatic_complexity",
                        1,
                    )
                )

            for class_data in classes:

                for method in class_data.get(
                    "methods",
                    []
                ):

                    all_complexities.append(
                        method.get(
                            "cyclomatic_complexity",
                            1,
                        )
                    )

            if (
                all_complexities
                and max(all_complexities) <= 5
            ):

                low_complexity_files += 1

        if low_complexity_files > 0:

            strengths.append(
                {
                    "title": "Low Code Complexity",
                    "message": (
                        f"{low_complexity_files} file(s) contain "
                        "functions or methods with relatively low "
                        "cyclomatic complexity."
                    )
                }
            )

        if summary["total_files"] > 0:

            strengths.append(
                {
                    "title": "Project Successfully Analyzed",
                    "message": (
                        f"The analyzer successfully processed "
                        f"{summary['total_files']} Python file(s) "
                        "and generated structural, dependency, "
                        "quality, and architectural insights."
                    )
                }
            )

        return strengths

    @staticmethod
    def generate_critical_issues(
        graph_analysis,
        architecture,
        recommendations,
    ):

        issues = []

        circular_dependencies = (
            graph_analysis.get(
                "circular_dependencies",
                []
            )
        )

        for cycle in circular_dependencies:

            if len(cycle) > 1:

                issues.append(
                    {
                        "type": "Circular Dependency",
                        "severity": "High",
                        "affected_modules": cycle[:-1],
                        "message": (
                            "A circular dependency exists between: "
                            + " → ".join(cycle)
                        )
                    }
                )

        for issue in architecture.get(
            "issues",
            []
        ):

            if issue["severity"] in [
                "High",
                "Medium",
            ]:

                issues.append(
                    {
                        "type": issue["type"],
                        "severity": issue["severity"],
                        "module": issue["module"],
                        "message": issue["message"],
                    }
                )

        for recommendation in recommendations:

            if (
                recommendation.get("priority")
                == "High"
            ):

                recommendation_issue = {
                    "type": recommendation.get(
                        "title"
                    ),
                    "severity": "High",
                    "message": recommendation.get(
                        "message"
                    ),
                }

                if "file" in recommendation:

                    recommendation_issue[
                        "file"
                    ] = recommendation["file"]

                if "module" in recommendation:

                    recommendation_issue[
                        "module"
                    ] = recommendation["module"]

                issues.append(
                    recommendation_issue
                )

        return issues

    @staticmethod
    def generate_architecture_summary(
        architecture
    ):

        layers = {}

        for layer, files in architecture[
            "layers"
        ].items():

            if files:

                layers[layer] = files

        core_modules = []

        for module_data in architecture[
            "core_modules"
        ]:

            core_modules.append(
                {
                    "module": module_data["module"],
                    "importance_score": module_data[
                        "importance_score"
                    ],
                }
            )

        return {
            "architecture_type": architecture[
                "architecture_type"
            ],
            "entry_points": architecture[
                "entry_points"
            ],
            "core_modules": core_modules,
            "detected_layers": layers,
        }

    @staticmethod
    def generate_recommended_actions(
        recommendations
    ):

        actions = []

        seen_titles = set()

        priority_order = {
            "High": 3,
            "Medium": 2,
            "Low": 1,
        }

        sorted_recommendations = sorted(
            recommendations,
            key=lambda item: priority_order.get(
                item.get("priority"),
                0,
            ),
            reverse=True,
        )

        for recommendation in sorted_recommendations:

            title = recommendation.get("title")

            if title in seen_titles:
                continue

            seen_titles.add(title)

            actions.append(
                {
                    "priority": recommendation.get(
                        "priority"
                    ),
                    "title": title,
                    "recommendation": recommendation.get(
                        "recommendation"
                    ),
                }
            )

        return actions

    @staticmethod
    def generate_file_summary(
        analysis
    ):

        files = []

        for file_data in analysis:

            files.append(
                {
                    "file": file_data["file"],
                    "maintainability": file_data[
                        "maintainability"
                    ],
                    "engineering_priority": file_data.get(
                        "engineering_priority",
                        {}
                    ),
                    "code_smell_count": len(
                        file_data.get(
                            "code_smells",
                            []
                        )
                    ),
                    "module_impact": file_data.get(
                        "module_impact",
                        {
                            "fan_in": 0,
                            "fan_out": 0,
                        }
                    ),
                }
            )

        files.sort(
            key=lambda item: item[
                "engineering_priority"
            ].get(
                "score",
                0,
            ),
            reverse=True,
        )

        return files