from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.project_analysis import ProjectAnalysis


class ProjectAnalysisService:

    @staticmethod
    def save_analysis(db: Session, project: Project, analysis: dict):
        project_health = analysis.get("project_health", {})
        architecture = analysis.get("architecture", {})
        graph_analysis = analysis.get("graph_analysis", {})

        circular_dependencies = graph_analysis.get("circular_dependencies", [])
        circular_count = len(circular_dependencies) if isinstance(circular_dependencies, list) else 0

        dependency_graph = analysis.get("dependency_graph", {})
        total_dependencies = sum(
            len(dependencies)
            for dependencies in dependency_graph.values()
            if isinstance(dependencies, list)
        )

        existing_analysis = (
            db.query(ProjectAnalysis)
            .filter(ProjectAnalysis.project_id == project.id)
            .first()
        )

        architecture_type = architecture.get(
            "architecture_type",
            architecture.get("type"),
        )

        if existing_analysis:
            existing_analysis.health_score = project_health.get("score", 0)
            existing_analysis.health_status = project_health.get("status", "Unknown")
            existing_analysis.architecture_type = architecture_type
            existing_analysis.total_dependencies = total_dependencies
            existing_analysis.circular_dependencies = circular_count
            existing_analysis.analysis_snapshot = analysis

            db.commit()
            db.refresh(existing_analysis)
            return existing_analysis

        project_analysis = ProjectAnalysis(
            health_score=project_health.get("score", 0),
            health_status=project_health.get("status", "Unknown"),
            architecture_type=architecture_type,
            total_dependencies=total_dependencies,
            circular_dependencies=circular_count,
            analysis_snapshot=analysis,
            project_id=project.id,
        )

        db.add(project_analysis)
        db.commit()
        db.refresh(project_analysis)
        return project_analysis
