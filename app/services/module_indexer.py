from pathlib import Path


class ModuleIndexer:

    @staticmethod
    def build(project_path: Path) -> set[str]:

        modules = set()

        # Detect the actual source root
        source_root = project_path

        children = [
            child for child in project_path.iterdir()
            if child.is_dir() and child.name != "__MACOSX"
        ]

        if len(children) == 1:
            source_root = children[0]

        for file in source_root.rglob("*.py"):

            if "__MACOSX" in file.parts:
                continue

            relative = file.relative_to(source_root)

            module = relative.with_suffix("")

            modules.add(".".join(module.parts))

        return modules