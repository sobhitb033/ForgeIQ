import zipfile
from pathlib import Path

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.dependencies.database import get_db
from app.models.user import User
from app.services.file_scanner import FileScanner
from app.services.project_service import ProjectService

router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/test")
def create_test_project(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ProjectService.create_project(
        db=db,
        project_name="Demo Project",
        current_user=current_user,
    )


@router.post("/upload")
async def upload_project(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    # Create project entry in database
    project = ProjectService.create_project(
        db=db,
        project_name=file.filename.replace(".zip", ""),
        current_user=current_user,
    )

    # Create folder structure
    user_folder = UPLOAD_DIR / f"user_{current_user.id}"
    project_folder = user_folder / f"project_{project.id}"

    project_folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Save uploaded ZIP
    file_path = project_folder / file.filename

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Update upload path in database
    project = ProjectService.update_upload_path(
        db=db,
        project=project,
        upload_path=str(file_path),
    )

    # Extract ZIP
    extract_folder = project_folder / "extracted"

    extract_folder.mkdir(
        exist_ok=True,
    )

    with zipfile.ZipFile(file_path, "r") as zip_ref:
        zip_ref.extractall(extract_folder)

    # Scan Python files
    python_files = FileScanner.find_python_files(
        extract_folder
    )

    return {
        "project": {
            "id": project.id,
            "project_name": project.project_name,
            "upload_path": project.upload_path,
            "status": project.status,
            "uploaded_at": project.uploaded_at,
        },
        "python_files": [
            str(file)
            for file in python_files
        ],
    }