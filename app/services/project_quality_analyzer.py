class ProjectQualityAnalyzer:

    @staticmethod
    def analyze(
        analysis: list[dict],
        graph_analysis: dict
    ):

        severity_summary = {
            "Low": 0,
            "Medium": 0,
            "High": 0,
            "Critical": 0,
        }

        for file in analysis:

            for smell in file["code_smells"]:

                severity = smell["severity"]

                if severity in severity_summary:
                    severity_summary[severity] += 1