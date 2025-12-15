from datetime import datetime
from typing import Optional


class Comment:
    def __init__(
        self,
        id: Optional[str] = None,
        project_id: str = "",
        user_id: str = "",
        content: str = "",
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id
        self.project_id = project_id
        self.user_id = user_id
        self.content = content
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

