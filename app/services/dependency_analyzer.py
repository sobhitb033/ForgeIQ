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

        for imported_module in ast_data["imports"]:

            # Ignore empty imports
            if not imported_module:
                continue

            # Check if the import directly matches
            if imported_module in project_modules:

                internal.append(imported_module)
                continue

            # Check whether the imported module is a parent
            # or child of a project module
            is_internal = any(
                module.startswith(imported_module + ".")
                or imported_module.startswith(module + ".")
                for module in project_modules
            )

            if is_internal:
                internal.append(imported_module)
            else:
                external.append(imported_module)

        return {
            "internal": list(set(internal)),
            "external": list(set(external)),
            "total_internal": len(set(internal)),
            "total_external": len(set(external)),
        }