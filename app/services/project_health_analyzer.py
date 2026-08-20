class ProjectHealthAnalyzer:

    @staticmethod
    def analyze(analysis, graph_analysis):

        total_files = len(analysis)

        if total_files == 0:
            return {
                "score": 100,
                "status": "Excellent",
                "factors": {
                    "average_maintainability": 100,
                    "total_code_smells": 0,
                    "circular_dependencies": 0,
                    "high_priority_files": 0
                }
            }

        maintainability_scores = []

        for file_data in analysis:
            maintainability_scores.append(
                file_data["maintainability"]["index"]
            )

        average_maintainability = (
            sum(maintainability_scores)
            / total_files
        )

        total_code_smells = sum(
            len(file_data["code_smells"])
            for file_data in analysis
        )

        circular_dependencies = len(
            graph_analysis["circular_dependencies"]
        )

        high_priority_files = sum(
            1
            for file_data in analysis
            if file_data["engineering_priority"]["priority"]
            in ["High", "Critical"]
        )

        score = average_maintainability

        # Penalize code smells
        score -= min(total_code_smells * 2, 20)

        # Penalize circular dependencies
        score -= min(circular_dependencies * 10, 20)

        # Penalize high-risk files
        score -= min(high_priority_files * 5, 20)

        # Keep score between 0 and 100
        score = max(0, min(round(score, 2), 100))

        if score >= 85:
            status = "Excellent"

        elif score >= 70:
            status = "Good"

        elif score >= 50:
            status = "Fair"

        else:
            status = "Poor"

        return {
            "score": score,
            "status": status,
            "factors": {
                "average_maintainability": round(
                    average_maintainability,
                    2
                ),
                "total_code_smells": total_code_smells,
                "circular_dependencies": circular_dependencies,
                "high_priority_files": high_priority_files
            }
        }