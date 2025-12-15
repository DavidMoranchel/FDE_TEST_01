from typing import Optional, List
from sqlalchemy.orm import Session
from app.domain.entities.project import Project
from app.domain.value_objects.project_status import ProjectStatus
from app.domain.repositories.project_repository import ProjectRepository
from app.infrastructure.models.project_model import ProjectModel
from datetime import datetime


class ProjectRepositoryImpl(ProjectRepository):
    def __init__(self, db: Session):
        self.db = db

    async def create(self, project: Project) -> Project:
        db_project = ProjectModel(
            title=project.title,
            description=project.description,
            status=project.status,
            client_id=project.client_id,
        )
        self.db.add(db_project)
        self.db.commit()
        self.db.refresh(db_project)
        return self._to_domain(db_project)

    def get_by_id(self, project_id: str) -> Optional[Project]:
        db_project = self.db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
        return self._to_domain(db_project) if db_project else None

    async def get_all(self) -> List[Project]:
        db_projects = self.db.query(ProjectModel).all()
        return [self._to_domain(p) for p in db_projects]

    async def get_by_client_id(self, client_id: str) -> List[Project]:
        db_projects = self.db.query(ProjectModel).filter(ProjectModel.client_id == client_id).all()
        return [self._to_domain(p) for p in db_projects]

    async def update(self, project: Project) -> Project:
        db_project = self.db.query(ProjectModel).filter(ProjectModel.id == project.id).first()
        if db_project:
            db_project.title = project.title
            db_project.description = project.description
            db_project.status = project.status
            db_project.client_id = project.client_id
            db_project.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(db_project)
            return self._to_domain(db_project)
        return project

    async def delete(self, project_id: str) -> bool:
        db_project = self.db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
        if db_project:
            self.db.delete(db_project)
            self.db.commit()
            return True
        return False

    def _to_domain(self, db_project: ProjectModel) -> Project:
        return Project(
            id=str(db_project.id),
            title=db_project.title,
            description=db_project.description,
            status=db_project.status,
            client_id=str(db_project.client_id) if db_project.client_id else None,
            created_at=db_project.created_at,
            updated_at=db_project.updated_at,
        )

