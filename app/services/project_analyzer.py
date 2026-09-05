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
from app.services.engineering_priority import EngineeringPriority
from app.services.module_impact_analyzer import ModuleImpactAnalyzer
from app.services.project_health_analyzer import ProjectHealthAnalyzer
from app.services.architecture_analyzer import ArchitectureAnalyzer
from app.services.recommendation_engine import RecommendationEngine

from app.services.project_report_generator import ProjectReportGenerator

from app.services.recommendation_summary import RecommendationSummary


class ProjectAnalyzer:

    @staticmethod
    def analyze_project(project_path: Path):

        # Find all Python files
        python_files = FileScanner.find_python_files(
            project_path
        )

        # Build module index
        project_modules = ModuleIndexer.build(
            project_path
        )

        analysis = []

        # Analyze every Python file
        for file in python_files:

            # Parse AST
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

            # Code smells
            code_smells = CodeSmellAnalyzer.analyze(
                ast_data["tree"]
            )

            # Dependencies
            dependencies = DependencyAnalyzer.analyze_file(
                file,
                ast_data,
                project_modules
            )

            # Remove raw AST before API response
            ast_data.pop("tree", None)

            analysis.append(
                {
                    "file": str(
                        file.relative_to(project_path)
                    ),
                    "ast": ast_data,
                    "metrics": metrics,
                    "maintainability": maintainability,
                    "dependencies": dependencies,
                    "code_smells": code_smells,
                }
            )

        # Build dependency graph
        dependency_graph = DependencyGraphBuilder.build(
            analysis
        )

        # Analyze dependency graph
        graph_analysis = GraphAnalyzer.analyze(
            dependency_graph
        )

        # Analyze module impact
        module_impact = ModuleImpactAnalyzer.analyze(
            dependency_graph
        )

        # Get circular dependencies
        circular_dependencies = graph_analysis[
            "circular_dependencies"
        ]

        # Calculate engineering priority
        for file_data in analysis:

            file_path = file_data["file"].replace(
                "\\", "/"
            )

            # Remove the top-level project folder
            relative_path = file_path

            # Convert path to Python module format
            module = (
                relative_path
                .removesuffix(".py")
                .replace("/", ".")
            )

            # Get module impact
            impact_data = module_impact.get(
                module,
                {
                    "fan_in": 0,
                    "fan_out": 0
                }
            )

            # Number of internal dependencies
            dependency_count = len(
                file_data["dependencies"]["internal"]
            )

            # Check circular dependency
            circular_dependency = False

            for cycle in circular_dependencies:

                if module in cycle:
                    circular_dependency = True
                    break

            # Calculate engineering priority
            priority = EngineeringPriority.calculate(
                ast_data=file_data["ast"],
                maintainability=file_data[
                    "maintainability"
                ],
                code_smells=file_data[
                    "code_smells"
                ],
                dependency_count=dependency_count,
                circular_dependency=circular_dependency,
                fan_in=impact_data["fan_in"],
                fan_out=impact_data["fan_out"],
                blast_radius=impact_data.get("blast_radius", 0)
            )

            # Add results to file analysis
            file_data[
                "engineering_priority"
            ] = priority

            file_data[
                "module_impact"
            ] = impact_data

        # Calculate project health
        # Engineering priority must exist first
        project_health = ProjectHealthAnalyzer.analyze(
            analysis,
            graph_analysis
        )

        # Analyze project architecture
        architecture = ArchitectureAnalyzer.analyze(
            analysis,
            dependency_graph,
            module_impact
        )

        # Generate recommendations
        recommendations = RecommendationEngine.generate(
            analysis,
            graph_analysis,
            project_health,
            architecture
        )

        recommendation_summary = RecommendationSummary.generate(
            recommendations
        )

        # Generate project summary
        summary = ProjectSummary.generate(
            analysis
        )

        #Generate structred project report
        project_report = ProjectReportGenerator.generate(
            summary=summary,
            project_health=project_health,
            architecture=architecture,
            graph_analysis=graph_analysis,
            recommendations=recommendations,
            analysis=analysis,
        )

        return {
            "summary": summary,
            "dependency_graph": dependency_graph,
            "graph_analysis": graph_analysis,
            "module_impact": module_impact,
            "project_health": project_health,
            "architecture": architecture,
            "recommendations": recommendations,
            "project_report": project_report,
            "files": analysis,
            "recommendation_summary": recommendation_summary,
        }