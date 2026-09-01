from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.project_analysis import ProjectAnalysis


class ProjectAnalysisService:

    @staticmethod
    def save_analysis(
        db: Session,
        project: Project,
        analysis: dict,
    ):

        project_health = analysis.get(
            "project_health",
            {}
        )

        architecture = analysis.get(
            "architecture",
            {}
        )

        graph_analysis = analysis.get(
            "graph_analysis",
            {}
        )

        # Count circular dependencies
        circular_dependencies = graph_analysis.get(
            "circular_dependencies",
            []
        )

        if isinstance(
            circular_dependencies,
            list,
        ):
            circular_count = len(
                circular_dependencies
            )
        else:
            circular_count = 0

        # Calculate total dependencies
        dependency_graph = analysis.get(
            "dependency_graph",
            {}
        )

        total_dependencies = sum(
            len(dependencies)
            for dependencies in dependency_graph.values()
            if isinstance(dependencies, list)
        )

        # Check if analysis already exists
        existing_analysis = (
            db.query(ProjectAnalysis)
            .filter(
                ProjectAnalysis.project_id == project.id
            )
            .first()
        )

        if existing_analysis:

            existing_analysis.health_score = (
                project_health.get("score", 0)
            )

            existing_analysis.health_status = (
                project_health.get(
                    "status",
                    "Unknown",
                )
            )

            existing_analysis.architecture_type = (
                architecture.get(
                    "architecture_type",
                    architecture.get(
                        "type",
                        None,
                    ),
                )
            )

            existing_analysis.total_dependencies = (
                total_dependencies
            )

            existing_analysis.circular_dependencies = (
                circular_count
            )

            db.commit()
            db.refresh(existing_analysis)

            return existing_analysis

        # Create new analysis record
        project_analysis = ProjectAnalysis(

            health_score=project_health.get(
                "score",
                0,
            ),

            health_status=project_health.get(
                "status",
                "Unknown",
            ),

            architecture_type=architecture.get(
                "architecture_type",
                architecture.get(
                    "type",
                    None,
                ),
            ),

            total_dependencies=total_dependencies,

            circular_dependencies=circular_count,

            project_id=project.id,
        )

        db.add(project_analysis)

        db.commit()

        db.refresh(project_analysis)

        return project_analysis