from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.dependencies.database import get_db

from app.models.user import User
from app.models.project import Project
from app.models.recommendation import Recommendation

from app.services.project_service import ProjectService
from app.services.upload_service import UploadService

from app.core.security import get_current_user


router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


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

    return await UploadService.upload_project(
        file=file,
        db=db,
        current_user=current_user,
    )


@router.get("/{project_id}/recommendations/summary")
def get_recommendation_summary(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    project = (
        db.query(Project)
        .filter(
            Project.id == project_id,
            Project.user_id == current_user.id,
        )
        .first()
    )

    if not project:

        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    recommendations = (
        db.query(Recommendation)
        .filter(
            Recommendation.project_id == project_id
        )
        .all()
    )

    priority_summary = {
        "Critical": 0,
        "High": 0,
        "Medium": 0,
        "Low": 0,
    }

    for recommendation in recommendations:

        priority = recommendation.priority

        if priority in priority_summary:

            priority_summary[priority] += 1

    priority_order = {
        "Critical": 1,
        "High": 2,
        "Medium": 3,
        "Low": 4,
    }

    sorted_recommendations = sorted(
        recommendations,
        key=lambda recommendation: priority_order.get(
            recommendation.priority,
            5,
        ),
    )

    top_recommendations = []

    for recommendation in sorted_recommendations[:10]:

        top_recommendations.append(
            {
                "id": recommendation.id,
                "priority": recommendation.priority,
                "title": recommendation.title,
                "message": recommendation.message,
                "recommendation": recommendation.recommendation,
            }
        )

    return {
        "project_id": project.id,
        "project_name": project.project_name,
        "total_recommendations": len(recommendations),
        "priority_summary": priority_summary,
        "top_recommendations": top_recommendations,
    }