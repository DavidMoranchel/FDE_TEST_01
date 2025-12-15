from typing import List
from app.domain.entities.comment import Comment
from app.domain.repositories.comment_repository import CommentRepository


class CommentService:
    def __init__(self, comment_repository: CommentRepository):
        self.comment_repository = comment_repository

    async def create_comment(self, project_id: str, user_id: str, content: str) -> Comment:
        comment = Comment(
            project_id=project_id,
            user_id=user_id,
            content=content,
        )
        return await self.comment_repository.create(comment)

    async def get_comments_by_project(self, project_id: str) -> List[Comment]:
        return await self.comment_repository.get_by_project_id(project_id)

