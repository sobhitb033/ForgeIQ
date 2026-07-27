class ProjectSummary:

    @staticmethod
    def generate(file_analysis: list[dict]):

        summary = {
            "total_files": len(file_analysis),
            "total_lines": 0,
            "code_lines": 0,
            "blank_lines": 0,
            "comment_lines": 0,
            "total_imports": 0,
            "total_classes": 0,
            "total_functions": 0,
            "total_methods": 0,
            "project_health": ""
        }

        for file in file_analysis:

            metrics = file["metrics"]

            summary["total_lines"] += metrics["total_lines"]
            summary["code_lines"] += metrics["code_lines"]
            summary["blank_lines"] += metrics["blank_lines"]
            summary["comment_lines"] += metrics["comment_lines"]
            summary["total_imports"] += metrics["imports"]
            summary["total_classes"] += metrics["classes"]
            summary["total_functions"] += metrics["functions"]
            summary["total_methods"] += metrics["methods"]

        health_score = 100

        health_score -= summary["blank_lines"] // 20
        health_score -= summary["total_methods"] // 30

        health_score = max(0, min(100, health_score))

        if health_score >= 90:
            health = "Excellent"
        elif health_score >= 75:
            health = "Good"
        elif health_score >= 60:
            health = "Fair"
        else:
            health = "Needs Improvement"

        summary["project_health"] = health

        return summary