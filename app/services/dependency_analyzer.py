from pathlib import Path


class DependencyAnalyzer:

    @staticmethod
    def analyze_file(
        file_path: Path,
        ast_data: dict,
        project_modules: set[str],
    ):

        internal = []
        external = []

        for module in ast_data["imports"]:

            if module in project_modules:
                internal.append(module)
            else:
                external.append(module)

        return {
            "internal": internal,
            "external": external,
            "total_internal": len(internal),
            "total_external": len(external),
        }