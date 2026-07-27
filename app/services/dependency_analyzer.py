from pathlib import Path


class DependencyAnalyzer:

    @staticmethod
    def analyze_file(
        file_path: Path,
        ast_data: dict,
    ):

        return {
            "imports": ast_data["imports"]
        }