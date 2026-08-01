import ast
from pathlib import Path

from app.services.complexity_analyzer import ComplexityAnalyzer


class ASTParser:

    @staticmethod
    def parse_file(file_path: Path):

        source = file_path.read_text(encoding="utf-8")
        tree = ast.parse(source)

        return {
            "imports": ASTParser.extract_imports(tree),
            "classes": ASTParser.extract_classes(tree),
            "functions": ASTParser.extract_functions(tree),
        }

    @staticmethod
    def extract_imports(tree):

        imports = []

        for node in ast.walk(tree):

            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)

            elif isinstance(node, ast.ImportFrom):
                imports.append(node.module or "")

        return imports

    @staticmethod
    def extract_classes(tree):

        classes = []

        # Only top-level classes
        for node in tree.body:

            if isinstance(node, ast.ClassDef):

                methods = []

                # Only methods inside this class
                for item in node.body:

                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):

                        parameters = [arg.arg for arg in item.args.args]

                        decorators = []

                        for decorator in item.decorator_list:
                            if isinstance(decorator, ast.Name):
                                decorators.append(decorator.id)

                        complexity = ComplexityAnalyzer.analyze(item)

                        if complexity <= 5:
                            risk = "Low"
                        elif complexity <= 10:
                            risk = "Moderate"
                        elif complexity <= 20:
                            risk = "High"
                        else:
                            risk = "Critical"

                        methods.append(
                            {
                                "name": item.name,
                                "parameters": parameters,
                                "return_type": None,
                                "decorators": decorators,
                                "is_async": isinstance(item, ast.AsyncFunctionDef),
                                "docstring": ast.get_docstring(item),
                                "line_number": item.lineno,
                                "cyclomatic_complexity": complexity,
                                "risk": risk,
                            }
                        )

                base_classes = []

                for base in node.bases:

                    if isinstance(base, ast.Name):
                        base_classes.append(base.id)

                    elif isinstance(base, ast.Attribute):
                        base_classes.append(base.attr)

                classes.append(
                    {
                        "name": node.name,
                        "line_number": node.lineno,
                        "base_classes": base_classes,
                        "docstring": ast.get_docstring(node),
                        "methods": methods,
                    }
                )

        return classes

    @staticmethod
    def extract_functions(tree):

        functions = []

        # Only module-level functions
        for node in tree.body:

            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):

                parameters = [arg.arg for arg in node.args.args]

                decorators = []

                for decorator in node.decorator_list:
                    if isinstance(decorator, ast.Name):
                        decorators.append(decorator.id)

                complexity = ComplexityAnalyzer.analyze(node)

                if complexity <= 5:
                    risk = "Low"
                elif complexity <= 10:
                    risk = "Moderate"
                elif complexity <= 20:
                    risk = "High"
                else:
                    risk = "Critical"

                functions.append(
                    {
                        "name": node.name,
                        "parameters": parameters,
                        "return_type": None,
                        "decorators": decorators,
                        "is_async": isinstance(node, ast.AsyncFunctionDef),
                        "docstring": ast.get_docstring(node),
                        "line_number": node.lineno,
                        "cyclomatic_complexity": complexity,
                        "risk": risk,
                    }
                )

        return functions