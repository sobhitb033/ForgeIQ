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

            imported_module = imported_module.strip()

            # 1. Exact match
            
            if imported_module in project_modules:
                internal.append(imported_module)
                continue

            # 2. Match short/local imports against full module names.

            matching_modules = [
                module
                for module in project_modules
                if module.endswith("." + imported_module)
            ]

            if len(matching_modules) == 1:
                internal.append(matching_modules[0])
                continue

            # 3. Handle package/parent imports.

            parent_matches = [
                module
                for module in project_modules
                if module.endswith("." + imported_module)
                or module.startswith(imported_module + ".")
            ]

            if parent_matches:
                parent_matches.sort(key=len)
                internal.append(parent_matches[0])
                continue

            # 4. Otherwise it is an external dependency.

            external.append(imported_module)

        # Remove duplicates
        internal = list(set(internal))
        external = list(set(external))

        return {
            "internal": internal,
            "external": external,
            "total_internal": len(internal),
            "total_external": len(external),
        }