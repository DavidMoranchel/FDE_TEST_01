from typing import List
from sqlalchemy.orm import Session
from app.domain.entities.comment import Comment
from app.domain.repositories.comment_repository import CommentRepository
from app.infrastructure.models.comment_model import CommentModel


class CommentRepositoryImpl(CommentRepository):
    def __init__(self, db: Session):
        self.db = db

    async def create(self, comment: Comment) -> Comment:
        db_comment = CommentModel(
            project_id=comment.project_id,
            user_id=comment.user_id,
            content=comment.content,
        )
        self.db.add(db_comment)
        self.db.commit()
        self.db.refresh(db_comment)
        return self._to_domain(db_comment)

    async def get_by_project_id(self, project_id: str) -> List[Comment]:
        db_comments = self.db.query(CommentModel).filter(CommentModel.project_id == project_id).order_by(CommentModel.created_at.desc()).all()
        return [self._to_domain(c) for c in db_comments]

    def _to_domain(self, db_comment: CommentModel) -> Comment:
        return Comment(
            id=str(db_comment.id),
            project_id=str(db_comment.project_id),
            user_id=str(db_comment.user_id),
            content=db_comment.content,
            created_at=db_comment.created_at,
            updated_at=db_comment.updated_at,
        )

