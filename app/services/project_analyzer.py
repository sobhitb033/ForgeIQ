from pathlib import Path

from app.services.file_scanner import FileScanner
from app.services.ast_parser import ASTParser


class ProjectAnalyzer:

    @staticmethod
    def analyze_project(project_folder: Path):

        python_files = FileScanner.find_python_files(
            project_folder
        )

        analysis = []

        for file in python_files:
            analysis.append(
                ASTParser.parse_file(file)
            )

        return analysis