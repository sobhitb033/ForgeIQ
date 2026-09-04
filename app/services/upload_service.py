import zipfile
from pathlib import Path

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models.user import User
from app.services.project_service import ProjectService
from app.services.project_analyzer import ProjectAnalyzer
from app.services.source_file_service import SourceFileService
from app.services.project_analysis_service import ProjectAnalysisService
from app.services.recommendation_service import RecommendationService


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


class UploadService:

    @staticmethod
    async def upload_project(file: UploadFile, db: Session, current_user: User):
        project = None

        try:
            if not file.filename.endswith(".zip"):
                raise ValueError("Only ZIP files are supported.")

            project = ProjectService.create_project(
                db=db,
                project_name=file.filename.replace(".zip", ""),
                current_user=current_user,
            )

            user_folder = UPLOAD_DIR / f"user_{current_user.id}"
            project_folder = user_folder / f"project_{project.id}"
            project_folder.mkdir(parents=True, exist_ok=True)

            file_path = project_folder / file.filename
            with open(file_path, "wb") as buffer:
                buffer.write(await file.read())

            project = ProjectService.update_upload_path(db, project, str(file_path))
            project = ProjectService.update_status(db, project, "Analyzing")

            extract_folder = project_folder / "extracted"
            extract_folder.mkdir(exist_ok=True)

            with zipfile.ZipFile(file_path, "r") as zip_ref:
                zip_ref.extractall(extract_folder)

            analysis = ProjectAnalyzer.analyze_project(extract_folder)

            RecommendationService.save_recommendations(
                db=db,
                project=project,
                recommendations=analysis["recommendations"],
            )

            project_analysis = ProjectAnalysisService.save_analysis(
                db=db,
                project=project,
                analysis=analysis,
            )

            SourceFileService.save_source_files(
                db=db,
                project=project,
                analysis=analysis["files"],
            )

            project = ProjectService.update_status(db, project, "Completed")

            return {
                "project": {
                    "id": project.id,
                    "project_name": project.project_name,
                    "upload_path": project.upload_path,
                    "status": project.status,
                    "uploaded_at": project.uploaded_at,
                },
                "analysis": {
                    "id": project_analysis.id,
                    "health_score": project_analysis.health_score,
                    "health_status": project_analysis.health_status,
                    "architecture_type": project_analysis.architecture_type,
                    "total_dependencies": project_analysis.total_dependencies,
                    "circular_dependencies": project_analysis.circular_dependencies,
                    "analyzed_at": project_analysis.analyzed_at,
                },
                "summary": analysis["summary"],
                "dependency_graph": analysis["dependency_graph"],
                "graph_analysis": analysis["graph_analysis"],
                "project_health": analysis["project_health"],
                "architecture": analysis["architecture"],
                "recommendations": analysis["recommendations"],
                "project_report": analysis["project_report"],
                "files": analysis["files"],
            }

        except Exception as error:
            if project is not None:
                ProjectService.update_status(db, project, "Failed")
            raise error
