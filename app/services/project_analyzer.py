from pathlib import Path

from app.services.file_scanner import FileScanner
from app.services.ast_parser import ASTParser
from app.services.metrics_engine import MetricsEngine

from app.services.project_summary import ProjectSummary


class ProjectAnalyzer:

    @staticmethod
    def analyze_project(project_path: Path):

        python_files = FileScanner.find_python_files(project_path)

        analysis = []

        for file in python_files:

            ast_data = ASTParser.parse_file(file)

            metrics = MetricsEngine.analyze_file(
                file,
                ast_data
            )

            analysis.append(
                {
                    "file": str(file.relative_to(project_path)),
                    "ast": ast_data,
                    "metrics": metrics,
                }
            )

        summary = ProjectSummary.generate(analysis)

        return {
            "summary": summary,
            "files": analysis
        }