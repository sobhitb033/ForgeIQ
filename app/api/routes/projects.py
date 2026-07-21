from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.dependencies.database import get_db
from app.models.user import User
from app.schemas.project import ProjectResponse
from app.services.project_service import ProjectService

router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


@router.post(
    "/test",
    response_model=ProjectResponse,
)
def create_test_project(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return ProjectService.create_project(
        db=db,
        project_name="Demo Project",
        upload_path="uploads/demo",
        current_user=current_user,
    )