from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.infrastructure.database import get_db
from app.application.services.comment_service import CommentService
from app.domain.repositories.comment_repository import CommentRepository
from app.infrastructure.repositories.comment_repository_impl import CommentRepositoryImpl
from app.adapters.api.v1.schemas import CommentCreate, CommentResponse
from app.adapters.api.v1.dependencies import get_current_user
from app.domain.entities.user import User
from app.application.services.project_service import ProjectService
from app.domain.repositories.project_repository import ProjectRepository
from app.infrastructure.repositories.project_repository_impl import ProjectRepositoryImpl
from app.domain.value_objects.user_role import UserRole
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl

router = APIRouter()


def get_comment_service(db: Session = Depends(get_db)) -> CommentService:
    comment_repo: CommentRepository = CommentRepositoryImpl(db)
    return CommentService(comment_repo)


def get_project_service(db: Session = Depends(get_db)) -> ProjectService:
    project_repo: ProjectRepository = ProjectRepositoryImpl(db)
    return ProjectService(project_repo)


@router.post("/{project_id}/comments", response_model=CommentResponse)
async def create_comment(
    project_id: str,
    comment_data: CommentCreate,
    current_user: User = Depends(get_current_user),
    comment_service: CommentService = Depends(get_comment_service),
    project_service: ProjectService = Depends(get_project_service),
):
    # Verify project exists and user has access
    project = await project_service.get_project(project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    # Check access for clients
    if current_user.role == UserRole.CLIENT and project.client_id != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    comment = await comment_service.create_comment(
        project_id=project_id,
        user_id=str(current_user.id),
        content=comment_data.content,
    )

    return CommentResponse(
        id=comment.id,
        project_id=comment.project_id,
        user_id=comment.user_id,
        user_name=current_user.name,
        content=comment.content,
        created_at=comment.created_at.isoformat(),
        updated_at=comment.updated_at.isoformat(),
    )


@router.get("/{project_id}/comments", response_model=List[CommentResponse])
async def get_comments(
    project_id: str,
    current_user: User = Depends(get_current_user),
    comment_service: CommentService = Depends(get_comment_service),
    project_service: ProjectService = Depends(get_project_service),
    db: Session = Depends(get_db),
):
    project = await project_service.get_project(project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    if current_user.role == UserRole.CLIENT and project.client_id != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    comments = await comment_service.get_comments_by_project(project_id)

    user_repo = UserRepositoryImpl(db)

    result = []
    for comment in comments:
        user = user_repo.get_by_id(comment.user_id)
        user_name = user.name if user else "Unknown"

        result.append(
            CommentResponse(
                id=comment.id,
                project_id=comment.project_id,
                user_id=comment.user_id,
                user_name=user_name,
                content=comment.content,
                created_at=comment.created_at.isoformat(),
                updated_at=comment.updated_at.isoformat(),
            )
        )
    return result

