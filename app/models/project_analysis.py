from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class ProjectAnalysis(Base):
    __tablename__ = "project_analyses"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    health_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    health_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    architecture_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    total_dependencies: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    circular_dependencies: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    analyzed_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id"),
        nullable=False,
    )

    project = relationship(
        "Project",
        back_populates="analysis",
    )