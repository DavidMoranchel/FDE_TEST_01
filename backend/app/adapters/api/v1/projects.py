from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.infrastructure.database import get_db
from app.application.services.project_service import ProjectService
from app.domain.repositories.project_repository import ProjectRepository
from app.infrastructure.repositories.project_repository_impl import ProjectRepositoryImpl
from app.adapters.api.v1.schemas import ProjectCreate, ProjectUpdate, ProjectResponse
from app.adapters.api.v1.dependencies import get_current_user
from app.domain.entities.user import User
from app.domain.value_objects.user_role import UserRole
from app.domain.value_objects.project_status import ProjectStatus
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl

router = APIRouter()


def get_project_service(db: Session = Depends(get_db)) -> ProjectService:
    project_repo: ProjectRepository = ProjectRepositoryImpl(db)
    return ProjectService(project_repo)


@router.post("", response_model=ProjectResponse)
async def create_project(
    project_data: ProjectCreate,
    current_user: User = Depends(get_current_user),
    service: ProjectService = Depends(get_project_service),
    db: Session = Depends(get_db),
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can create projects")

    project = await service.create_project(
        title=project_data.title,
        description=project_data.description,
        status=project_data.status,
        client_id=project_data.client_id,
    )

    # Get client name if client_id exists
    client_name = None
    if project.client_id:
        user_repo = UserRepositoryImpl(db)
        client = user_repo.get_by_id(project.client_id)
        client_name = client.name if client else None

    return ProjectResponse(
        id=project.id,
        title=project.title,
        description=project.description,
        status=project.status.value,
        client_id=project.client_id,
        client_name=client_name,
        created_at=project.created_at.isoformat(),
        updated_at=project.updated_at.isoformat(),
    )


@router.get("", response_model=List[ProjectResponse])
async def get_projects(
    current_user: User = Depends(get_current_user),
    service: ProjectService = Depends(get_project_service),
    db: Session = Depends(get_db),
):
    projects = await service.get_all_projects(current_user.role, str(current_user.id))

    # Get client names
    user_repo = UserRepositoryImpl(db)

    result = []
    for project in projects:
        client_name = None
        if project.client_id:
            client = user_repo.get_by_id(project.client_id)
            client_name = client.name if client else None

        result.append(
            ProjectResponse(
                id=project.id,
                title=project.title,
                description=project.description,
                status=project.status.value,
                client_id=project.client_id,
                client_name=client_name,
                created_at=project.created_at.isoformat(),
                updated_at=project.updated_at.isoformat(),
            )
        )
    return result


@router.get("/my-projects", response_model=List[ProjectResponse])
async def get_my_projects(
    current_user: User = Depends(get_current_user),
    service: ProjectService = Depends(get_project_service),
    db: Session = Depends(get_db),
):
    if current_user.role != UserRole.CLIENT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only clients can access this endpoint")

    projects = await service.get_all_projects(current_user.role, str(current_user.id))

    result = []
    for project in projects:
        result.append(
            ProjectResponse(
                id=project.id,
                title=project.title,
                description=project.description,
                status=project.status.value,
                client_id=project.client_id,
                client_name=None,
                created_at=project.created_at.isoformat(),
                updated_at=project.updated_at.isoformat(),
            )
        )
    return result


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: str,
    current_user: User = Depends(get_current_user),
    service: ProjectService = Depends(get_project_service),
    db: Session = Depends(get_db),
):
    project = await service.get_project(project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    # Check access
    if current_user.role == UserRole.CLIENT and project.client_id != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    # Get client name if client_id exists
    client_name = None
    if project.client_id:
        user_repo = UserRepositoryImpl(db)
        client = user_repo.get_by_id(project.client_id)
        client_name = client.name if client else None

    return ProjectResponse(
        id=project.id,
        title=project.title,
        description=project.description,
        status=project.status.value,
        client_id=project.client_id,
        client_name=client_name,
        created_at=project.created_at.isoformat(),
        updated_at=project.updated_at.isoformat(),
    )


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    project_data: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    service: ProjectService = Depends(get_project_service),
    db: Session = Depends(get_db),
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can update projects")

    project = await service.update_project(
        project_id=project_id,
        title=project_data.title,
        description=project_data.description,
        status=project_data.status,
        client_id=project_data.client_id,
    )

    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    # Get client name if client_id exists
    client_name = None
    if project.client_id:
        user_repo = UserRepositoryImpl(db)
        client = user_repo.get_by_id(project.client_id)
        client_name = client.name if client else None

    return ProjectResponse(
        id=project.id,
        title=project.title,
        description=project.description,
        status=project.status.value,
        client_id=project.client_id,
        client_name=client_name,
        created_at=project.created_at.isoformat(),
        updated_at=project.updated_at.isoformat(),
    )


@router.delete("/{project_id}")
async def delete_project(
    project_id: str,
    current_user: User = Depends(get_current_user),
    service: ProjectService = Depends(get_project_service),
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can delete projects")

    success = await service.delete_project(project_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    return {"message": "Project deleted successfully"}

