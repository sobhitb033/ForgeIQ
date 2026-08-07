from pathlib import Path

from app.services.file_scanner import FileScanner
from app.services.ast_parser import ASTParser
from app.services.metrics_engine import MetricsEngine
from app.services.dependency_analyzer import DependencyAnalyzer
from app.services.project_summary import ProjectSummary
from app.services.module_indexer import ModuleIndexer
from app.services.dependency_graph_builder import DependencyGraphBuilder
from app.services.graph_analyzer import GraphAnalyzer
from app.services.maintainability_analyzer import MaintainabilityAnalyzer

from app.services.code_smell_analyzer import CodeSmellAnalyzer


class ProjectAnalyzer:

    @staticmethod
    def analyze_project(project_path: Path):

        python_files = FileScanner.find_python_files(project_path)

        project_modules = ModuleIndexer.build(project_path)

        analysis = []

        for file in python_files:

            # Parse AST once
            ast_data = ASTParser.parse_file(file)

            # Metrics
            metrics = MetricsEngine.analyze_file(
                file,
                ast_data
            )

            # Maintainability
            maintainability = MaintainabilityAnalyzer.analyze(
                metrics
            )

            dependencies = DependencyAnalyzer.analyze_file(
                file,
                ast_data,
                project_modules
            )

            code_smells = CodeSmellAnalyzer.analyze(
                ast_data["tree"]
            )

            #Remove raw ast data before returning JSON
            ast_data.pop("tree",None)

            analysis.append(
                {
                    "file": str(file.relative_to(project_path)),
                    "ast": ast_data,
                    "metrics": metrics,
                    "maintainability": maintainability,
                    "dependencies": dependencies,
                    "code_smells": code_smells,
                }
            )

        # Project Summary
        summary = ProjectSummary.generate(
            analysis
        )

        # Dependency Graph
        dependency_graph = DependencyGraphBuilder.build(
            analysis
        )

        # Graph Analysis
        graph_analysis = GraphAnalyzer.analyze(
            dependency_graph
        )

        return {
            "summary": summary,
            "dependency_graph": dependency_graph,
            "graph_analysis": graph_analysis,
            "files": analysis,
        }