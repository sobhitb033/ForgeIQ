from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.user import User


class ProjectService:

    @staticmethod
    def create_project(
        db: Session,
        project_name: str,
        upload_path: str,
        current_user: User,
    ):

        project = Project(
            project_name=project_name,
            upload_path=upload_path,
            user_id=current_user.id,
        )

        db.add(project)
        db.commit()
        db.refresh(project)

        return project