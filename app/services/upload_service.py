import zipfile
from pathlib import Path

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models.user import User
from app.services.project_service import ProjectService
from app.services.project_analyzer import ProjectAnalyzer


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


class UploadService:

    @staticmethod
    async def upload_project(
        file: UploadFile,
        db: Session,
        current_user: User,
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

        # Analyze project
        analysis = ProjectAnalyzer.analyze_project(
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
            "summary": analysis["summary"],
            "analysis": analysis["files"],
        }