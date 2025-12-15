from datetime import datetime
from typing import Optional
from app.domain.value_objects.user_role import UserRole


class User:
    def __init__(
        self,
        id: Optional[str] = None,
        email: str = "",
        name: str = "",
        hashed_password: str = "",
        role: UserRole = UserRole.CLIENT,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id
        self.email = email
        self.name = name
        self.hashed_password = hashed_password
        self.role = role
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

