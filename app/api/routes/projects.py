from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.dependencies.database import get_db
from app.models.user import User
from app.schemas.project import ProjectResponse
from app.services.project_service import ProjectService

from pathlib import Path

from fastapi import File, UploadFile

router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


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

@router.post(
    "/upload",
    response_model=ProjectResponse,
)
async def upload_project(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    project = ProjectService.create_project(
        db=db,
        project_name=file.filename.replace(".zip", ""),
        current_user=current_user,
    )

    user_folder = UPLOAD_DIR / f"user_{current_user.id}"

    project_folder = (
        user_folder /
        f"project_{project.id}"
    )

    project_folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_path = (
        project_folder /
        file.filename
    )

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    project = ProjectService.update_upload_path(
        db,
        project,
        str(file_path),
    )

    return project