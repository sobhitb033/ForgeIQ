from datetime import datetime

from pydantic import BaseModel


class ProjectResponse(BaseModel):
    id: int
    project_name: str
    upload_path: str
    status: str
    uploaded_at: datetime

    model_config = {
        "from_attributes": True
    }