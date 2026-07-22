import ast
from pathlib import Path


class ASTParser:

    @staticmethod
    def parse_file(file_path: Path):

        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()
        print("=" * 50)
        print("FILE BEING PARSED:")
        print(file_path)
        print("=" * 50)
        print(source)
        print("=" * 50)

        tree = ast.parse(source)

        tree = ast.parse(source)

        imports = []
        classes = []
        functions = []

        for node in ast.walk(tree):

            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)

            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                imports.append(module)

            elif isinstance(node, ast.ClassDef):
                classes.append(node.name)

            elif isinstance(node, ast.FunctionDef):
                functions.append(node.name)

        return {
            "file": str(file_path),
            "imports": imports,
            "classes": classes,
            "functions": functions,
        }