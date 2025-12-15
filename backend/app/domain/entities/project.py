from datetime import datetime
from typing import Optional
from app.domain.value_objects.project_status import ProjectStatus


class Project:
    def __init__(
        self,
        id: Optional[str] = None,
        title: str = "",
        description: str = "",
        status: ProjectStatus = ProjectStatus.ACTIVE,
        client_id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.client_id = client_id
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

