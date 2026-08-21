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

        return summary