from pathlib import Path


class ModuleIndexer:

    @staticmethod
    def build(project_path: Path) -> set[str]:

        modules = set()

        for file in project_path.rglob("*.py"):

            if "__MACOSX" in file.parts:
                continue

            relative = file.relative_to(project_path)

            # Remove .py
            module = relative.with_suffix("")

            # Convert:
            # app/services/graph_utils.py
            #
            # to:
            # app.services.graph_utils

            module_name = ".".join(module.parts)

            modules.add(module_name)

        return modules