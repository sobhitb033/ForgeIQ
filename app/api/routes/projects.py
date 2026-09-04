from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.models.user import User
from app.models.project import Project
from app.models.recommendation import Recommendation
from app.services.project_service import ProjectService
from app.services.upload_service import UploadService
from app.core.security import get_current_user


router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/test")
def create_test_project(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return ProjectService.create_project(db=db, project_name="Demo Project", current_user=current_user)


@router.post("/upload")
async def upload_project(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await UploadService.upload_project(file=file, db=db, current_user=current_user)


@router.get("")
def list_projects(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return {"projects": ProjectService.list_user_projects(db, current_user)}


@router.get("/{project_id}")
def get_project(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = ProjectService.get_user_project(db, project_id, current_user)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return ProjectService.get_project_workspace(db, project)


@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = ProjectService.get_user_project(db, project_id, current_user)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    ProjectService.delete_project(db, project)
    return {"message": "Project deleted successfully", "project_id": project_id}


@router.get("/{project_id}/recommendations/summary")
def get_recommendation_summary(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = ProjectService.get_user_project(db, project_id, current_user)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    recommendations = db.query(Recommendation).filter(Recommendation.project_id == project_id).all()
    priority_summary = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
    for recommendation in recommendations:
        if recommendation.priority in priority_summary:
            priority_summary[recommendation.priority] += 1

    priority_order = {"Critical": 1, "High": 2, "Medium": 3, "Low": 4}
    sorted_recommendations = sorted(
        recommendations,
        key=lambda recommendation: priority_order.get(recommendation.priority, 5),
    )

    top_recommendations = [
        {
            "id": recommendation.id,
            "priority": recommendation.priority,
            "title": recommendation.title,
            "message": recommendation.message,
            "recommendation": recommendation.recommendation,
        }
        for recommendation in sorted_recommendations[:10]
    ]

    return {
        "project_id": project.id,
        "project_name": project.project_name,
        "total_recommendations": len(recommendations),
        "priority_summary": priority_summary,
        "top_recommendations": top_recommendations,
    }
