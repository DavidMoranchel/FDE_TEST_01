from typing import List, Optional
from app.domain.entities.project import Project
from app.domain.value_objects.project_status import ProjectStatus
from app.domain.repositories.project_repository import ProjectRepository
from app.domain.value_objects.user_role import UserRole


class ProjectService:
    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository

    async def create_project(
        self, title: str, description: str, status: ProjectStatus, client_id: Optional[str] = None
    ) -> Project:
        project = Project(
            title=title,
            description=description,
            status=status,
            client_id=client_id,
        )
        return await self.project_repository.create(project)

    async def get_project(self, project_id: str) -> Optional[Project]:
        return self.project_repository.get_by_id(project_id)

    async def get_all_projects(self, user_role: UserRole, user_id: Optional[str] = None) -> List[Project]:
        if user_role == UserRole.ADMIN:
            return await self.project_repository.get_all()
        elif user_role == UserRole.CLIENT and user_id:
            return await self.project_repository.get_by_client_id(user_id)
        return []

    async def update_project(
        self,
        project_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[ProjectStatus] = None,
        client_id: Optional[str] = None,
    ) -> Optional[Project]:
        project = self.project_repository.get_by_id(project_id)
        if not project:
            return None

        if title is not None:
            project.title = title
        if description is not None:
            project.description = description
        if status is not None:
            project.status = status
        if client_id is not None:
            project.client_id = client_id

        return await self.project_repository.update(project)

    async def delete_project(self, project_id: str) -> bool:
        return await self.project_repository.delete(project_id)

