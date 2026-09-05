from datetime import timezone

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.project_analysis import ProjectAnalysis
from app.models.recommendation import Recommendation
from app.models.source_file import SourceFile
from app.models.user import User


class ProjectService:

    @staticmethod
    def _utc_iso(value):
        """Serialize a database UTC timestamp with an explicit UTC offset."""
        if value is None:
            return None
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        else:
            value = value.astimezone(timezone.utc)
        return value.isoformat()

    @staticmethod
    def create_project(db: Session, project_name: str, current_user: User):
        project = Project(
            project_name=project_name,
            upload_path="",
            status="Uploaded",
            user_id=current_user.id,
        )
        db.add(project)
        db.commit()
        db.refresh(project)
        return project

    @staticmethod
    def update_upload_path(db: Session, project: Project, upload_path: str):
        project.upload_path = upload_path
        db.commit()
        db.refresh(project)
        return project

    @staticmethod
    def update_status(db: Session, project: Project, status: str):
        project.status = status
        db.commit()
        db.refresh(project)
        return project

    @staticmethod
    def list_user_projects(db: Session, current_user: User):
        projects = (
            db.query(Project)
            .filter(Project.user_id == current_user.id)
            .order_by(Project.uploaded_at.desc())
            .all()
        )

        result = []
        for project in projects:
            analysis = (
                db.query(ProjectAnalysis)
                .filter(ProjectAnalysis.project_id == project.id)
                .first()
            )
            recommendation_count = (
                db.query(func.count(Recommendation.id))
                .filter(Recommendation.project_id == project.id)
                .scalar()
                or 0
            )

            result.append({
                "id": project.id,
                "project_name": project.project_name,
                "status": project.status,
                "uploaded_at": ProjectService._utc_iso(project.uploaded_at),
                "health_score": analysis.health_score if analysis else None,
                "health_status": analysis.health_status if analysis else None,
                "architecture_type": analysis.architecture_type if analysis else None,
                "total_dependencies": analysis.total_dependencies if analysis else 0,
                "circular_dependencies": analysis.circular_dependencies if analysis else 0,
                "recommendation_count": recommendation_count,
            })

        return result

    @staticmethod
    def get_user_project(db: Session, project_id: int, current_user: User):
        return (
            db.query(Project)
            .filter(
                Project.id == project_id,
                Project.user_id == current_user.id,
            )
            .first()
        )

    @staticmethod
    def get_project_workspace(db: Session, project: Project):
        analysis = (
            db.query(ProjectAnalysis)
            .filter(ProjectAnalysis.project_id == project.id)
            .first()
        )
        source_files = (
            db.query(SourceFile)
            .filter(SourceFile.project_id == project.id)
            .all()
        )
        recommendations = (
            db.query(Recommendation)
            .filter(Recommendation.project_id == project.id)
            .all()
        )

        analysis_snapshot = analysis.analysis_snapshot if analysis else None

        return {
            "project": {
                "id": project.id,
                "project_name": project.project_name,
                "upload_path": project.upload_path,
                "status": project.status,
                "uploaded_at": ProjectService._utc_iso(project.uploaded_at),
            },
            "analysis": {
                "id": analysis.id if analysis else None,
                "health_score": analysis.health_score if analysis else None,
                "health_status": analysis.health_status if analysis else None,
                "architecture_type": analysis.architecture_type if analysis else None,
                "total_dependencies": analysis.total_dependencies if analysis else 0,
                "circular_dependencies": analysis.circular_dependencies if analysis else 0,
                "analyzed_at": ProjectService._utc_iso(analysis.analyzed_at) if analysis else None,
            },
            "analysis_snapshot": analysis_snapshot,
            "source_files": [
                {
                    "id": source_file.id,
                    "file_name": source_file.file_name,
                    "file_path": source_file.file_path,
                    "file_type": source_file.file_type,
                    "total_lines": source_file.total_lines,
                    "code_lines": source_file.code_lines,
                    "created_at": ProjectService._utc_iso(source_file.created_at),
                }
                for source_file in source_files
            ],
            "recommendations": [
                {
                    "id": recommendation.id,
                    "priority": recommendation.priority,
                    "title": recommendation.title,
                    "message": recommendation.message,
                    "recommendation": recommendation.recommendation,
                    "created_at": ProjectService._utc_iso(recommendation.created_at),
                }
                for recommendation in recommendations
            ],
        }

    @staticmethod
    def delete_project(db: Session, project: Project):
        db.delete(project)
        db.commit()
