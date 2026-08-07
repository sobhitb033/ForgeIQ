import ast


class CodeSmellAnalyzer:

    @staticmethod
    def analyze(tree: ast.AST):

        smells = []

        smells.extend(
            CodeSmellAnalyzer.detect_long_functions(tree)
        )

        smells.extend(
            CodeSmellAnalyzer.detect_long_parameter_list(tree)
        )

        smells.extend(
            CodeSmellAnalyzer.detect_missing_docstrings(tree)
        )

        smells.extend(
            CodeSmellAnalyzer.detect_large_classes(tree)
        )

        return smells

    @staticmethod
    def detect_long_functions(tree):

        smells = []

        for node in ast.walk(tree):

            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):

                if hasattr(node, "end_lineno"):

                    length = node.end_lineno - node.lineno + 1

                    if length > 40:

                        smells.append(
                            {
                                "type": "Long Function",
                                "severity": "Medium",
                                "location": node.name,
                                "message": f"Function '{node.name}' contains {length} lines."
                            }
                        )

        return smells

    @staticmethod
    def detect_long_parameter_list(tree):

        smells = []

        for node in ast.walk(tree):

            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):

                parameter_count = len(node.args.args)

                if parameter_count > 5:

                    smells.append(
                        {
                            "type": "Long Parameter List",
                            "severity": "Medium",
                            "location": node.name,
                            "message": f"Function '{node.name}' has {parameter_count} parameters."
                        }
                    )

        return smells

    @staticmethod
    def detect_missing_docstrings(tree):

        smells = []

        for node in ast.walk(tree):

            if isinstance(node, ast.ClassDef):

                if ast.get_docstring(node) is None:

                    smells.append(
                        {
                            "type": "Missing Docstring",
                            "severity": "Low",
                            "location": node.name,
                            "message": f"'{node.name}' has no docstring."
                        }
                    )

            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):

                # Ignore constructors
                if node.name == "__init__":
                    continue

                if ast.get_docstring(node) is None:

                    smells.append(
                        {
                            "type": "Missing Docstring",
                            "severity": "Low",
                            "location": node.name,
                            "message": f"'{node.name}' has no docstring."
                        }
                    )

        return smells

    @staticmethod
    def detect_large_classes(tree):

        smells = []

        for node in ast.walk(tree):

            if isinstance(node, ast.ClassDef):

                methods = [
                    method
                    for method in node.body
                    if isinstance(method, (ast.FunctionDef, ast.AsyncFunctionDef))
                ]

                if len(methods) > 10:

                    smells.append(
                        {
                            "type": "Large Class",
                            "severity": "High",
                            "location": node.name,
                            "message": f"Class '{node.name}' contains {len(methods)} methods."
                        }
                    )

        return smells