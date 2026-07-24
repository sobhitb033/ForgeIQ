from pathlib import Path


class MetricsEngine:

    @staticmethod
    def analyze_file(file_path: Path, ast_data: dict):

        source = file_path.read_text(encoding="utf-8")
        lines = source.splitlines()

        total_lines = len(lines)

        blank_lines = 0
        comment_lines = 0

        for line in lines:

            stripped = line.strip()

            if stripped == "":
                blank_lines += 1

            elif stripped.startswith("#"):
                comment_lines += 1

        code_lines = total_lines - blank_lines - comment_lines

        imports = len(ast_data["imports"])
        classes = len(ast_data["classes"])
        functions = len(ast_data["functions"])

        methods = 0

        for cls in ast_data["classes"]:
            methods += len(cls["methods"])

        return {
            "total_lines": total_lines,
            "code_lines": code_lines,
            "blank_lines": blank_lines,
            "comment_lines": comment_lines,
            "imports": imports,
            "classes": classes,
            "functions": functions,
            "methods": methods,
        }