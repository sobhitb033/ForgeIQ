from pathlib import Path

from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.source_file import SourceFile


class SourceFileService:

    @staticmethod
    def save_source_files(
        db: Session,
        project: Project,
        analysis: list,
    ):

        source_files = []

        for file_data in analysis:

            file_path = file_data.get(
                "file",
                ""
            )

            metrics = file_data.get(
                "metrics",
                {}
            )

            path_object = Path(file_path)

            source_file = SourceFile(
                file_name=path_object.name,
                file_path=file_path,
                file_type=path_object.suffix.replace(
                    ".",
                    ""
                ),
                total_lines=metrics.get(
                    "total_lines",
                    0
                ),
                code_lines=metrics.get(
                    "code_lines",
                    0
                ),
                project_id=project.id,
            )

            source_files.append(
                source_file
            )

        db.add_all(source_files)

        db.commit()

        return source_files