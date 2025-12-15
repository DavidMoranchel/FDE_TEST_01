from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.project import Project


class ProjectRepository(ABC):
    @abstractmethod
    async def create(self, project: Project) -> Project:
        pass

    @abstractmethod
    def get_by_id(self, project_id: str) -> Optional[Project]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Project]:
        pass

    @abstractmethod
    async def get_by_client_id(self, client_id: str) -> List[Project]:
        pass

    @abstractmethod
    async def update(self, project: Project) -> Project:
        pass

    @abstractmethod
    async def delete(self, project_id: str) -> bool:
        pass

