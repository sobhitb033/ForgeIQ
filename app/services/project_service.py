from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.user import User


class ProjectService:

    @staticmethod
    def create_project(
        db: Session,
        project_name: str,
        current_user: User,
    ):

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
    def update_upload_path(
        db: Session,
        project: Project,
        upload_path: str,
    ):

        project.upload_path = upload_path

        db.commit()
        db.refresh(project)

        return project


    @staticmethod
    def update_status(
        db: Session,
        project: Project,
        status: str,
    ):

        project.status = status

        db.commit()
        db.refresh(project)

        return project