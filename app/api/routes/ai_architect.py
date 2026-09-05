from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import get_current_user
from app.dependencies.database import get_db
from app.models.project import Project
from app.models.project_analysis import ProjectAnalysis
from app.models.user import User
from app.services.ai_architect_service import AIArchitectService

router = APIRouter(prefix="/projects", tags=["AI Architect"])


class AIArchitectHistoryItem(BaseModel):
    role: str = Field(pattern="^(user|assistant)$")
    content: str = Field(min_length=1, max_length=4000)


class AIArchitectFocus(BaseModel):
    kind: str = Field(default="module", pattern="^(module|smell|recommendation)$")
    target: str = Field(min_length=1, max_length=500)
    title: str | None = Field(default=None, max_length=500)
    smell_type: str | None = Field(default=None, max_length=200)


class AIArchitectRequest(BaseModel):
    question: str | None = Field(default=None, max_length=4000)
    history: list[AIArchitectHistoryItem] = Field(default_factory=list, max_length=8)
    focus: AIArchitectFocus | None = None


@router.post("/{project_id}/ai-architect")
async def ask_ai_architect(
    project_id: int,
    request: AIArchitectRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = (
        db.query(Project)
        .filter(Project.id == project_id, Project.user_id == current_user.id)
        .first()
    )
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if not settings.AI_ENABLED:
        raise HTTPException(status_code=503, detail="AI Architect is disabled. Set AI_ENABLED=true in the backend environment.")
    if not settings.AI_API_KEY:
        raise HTTPException(status_code=503, detail="AI Architect is not configured. Set AI_API_KEY in the backend environment.")
    if not settings.AI_MODEL:
        raise HTTPException(status_code=503, detail="AI Architect is not configured. Set AI_MODEL in the backend environment.")

    analysis = db.query(ProjectAnalysis).filter(ProjectAnalysis.project_id == project.id).first()
    if not analysis or not analysis.analysis_snapshot:
        raise HTTPException(status_code=409, detail="This project does not have a stored analysis snapshot. Re-analyze the project first.")

    try:
        assessment = await AIArchitectService.analyze(
            snapshot=analysis.analysis_snapshot,
            api_key=settings.AI_API_KEY,
            base_url=settings.AI_BASE_URL,
            model=settings.AI_MODEL,
            question=request.question,
            history=[item.model_dump() for item in request.history],
            focus=request.focus.model_dump() if request.focus else None,
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"AI Architect request failed: {str(exc)}") from exc

    return {
        "project_id": project.id,
        "project_name": project.project_name,
        "question": request.question,
        "assessment": assessment,
    }
