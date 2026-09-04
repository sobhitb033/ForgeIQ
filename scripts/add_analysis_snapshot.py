import sys
from pathlib import Path

# Add the backend root (/app) to Python's import path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import inspect, text

from app.database.engine import engine


TABLE_NAME = "project_analyses"
COLUMN_NAME = "analysis_snapshot"


def main():
    inspector = inspect(engine)

    columns = {
        column["name"]
        for column in inspector.get_columns(TABLE_NAME)
    }

    if COLUMN_NAME in columns:
        print(
            f"{TABLE_NAME}.{COLUMN_NAME} already exists. Nothing to do."
        )
        return

    with engine.begin() as connection:
        connection.execute(
            text(
                f"ALTER TABLE {TABLE_NAME} "
                f"ADD COLUMN {COLUMN_NAME} JSON NULL"
            )
        )

    print(
        f"Added {TABLE_NAME}.{COLUMN_NAME} successfully."
    )


if __name__ == "__main__":
    main()