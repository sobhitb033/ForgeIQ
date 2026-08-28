from app.database.base import Base
from app.database.engine import engine

# Import all models so SQLAlchemy registers them
from app.models import User, Project, SourceFile


Base.metadata.create_all(bind=engine)

print("Database tables created successfully.")