from pathlib import Path

from app.services.file_scanner import FileScanner
from app.services.ast_parser import ASTParser
from app.services.metrics_engine import MetricsEngine
from app.services.dependency_analyzer import DependencyAnalyzer
from app.services.project_summary import ProjectSummary

from app.services.module_indexer import ModuleIndexer

from app.services.dependency_graph_builder import DependencyGraphBuilder

from app.services.graph_analyzer import GraphAnalyzer


class ProjectAnalyzer:

    @staticmethod
    def analyze_project(project_path: Path):

        python_files = FileScanner.find_python_files(project_path)
        project_modules = ModuleIndexer.build(project_path)
        print(project_modules)

        analysis = []

        for file in python_files:

            # Parse AST once
            ast_data = ASTParser.parse_file(file)

            # Generate metrics
            metrics = MetricsEngine.analyze_file(
                file,
                ast_data
            )

            # Analyze dependencies
            dependencies = DependencyAnalyzer.analyze_file(
                file,
                ast_data,
                project_modules
            )

            analysis.append(
                {
                    "file": str(file.relative_to(project_path)),
                    "ast": ast_data,
                    "metrics": metrics,
                    "dependencies": dependencies,
                }
            )

        # Generate project summary
        summary = ProjectSummary.generate(analysis)

        dependency_graph = DependencyGraphBuilder.build(
            analysis
        )

        graph_analysis = GraphAnalyzer.analyze(
            dependency_graph
        )

        return {
            "summary": summary,
            "dependency_graph": dependency_graph,
            "graph_analysis": graph_analysis,
            "files": analysis,
        }