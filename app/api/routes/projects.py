from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.models.user import User

from app.services.project_service import ProjectService
from app.services.upload_service import UploadService

router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


@router.post("/test")
def create_test_project(
    db: Session = Depends(get_db),
):
    current_user = db.query(User).first()

    return ProjectService.create_project(
        db=db,
        project_name="Demo Project",
        current_user=current_user,
    )


@router.post("/upload")
async def upload_project(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    current_user = db.query(User).first()

    return await UploadService.upload_project(
        file=file,
        db=db,
        current_user=current_user,
    )