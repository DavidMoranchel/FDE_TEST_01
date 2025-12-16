from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.comment import Comment


class CommentRepository(ABC):
    @abstractmethod
    async def create(self, comment: Comment) -> Comment:
        pass  # pragma: no cover

    @abstractmethod
    async def get_by_project_id(self, project_id: str) -> List[Comment]:
        pass  # pragma: no cover

