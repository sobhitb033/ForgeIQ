from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    project_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    upload_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="Uploaded",
    )

    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    owner = relationship(
        "User",
        back_populates="projects",
    )

    source_files = relationship(
        "SourceFile",
        back_populates="project",
        cascade="all, delete-orphan",
    )

    analysis = relationship(
        "ProjectAnalysis",
        back_populates="project",
        cascade="all, delete",
    )

    recommendations = relationship(
        "Recommendation",
        back_populates="project",
        cascade="all, delete",
    )