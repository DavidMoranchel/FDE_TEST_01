from typing import Optional, List
from sqlalchemy.orm import Session
from app.domain.entities.user import User
from app.domain.value_objects.user_role import UserRole
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.models.user_model import UserModel
from datetime import datetime


class UserRepositoryImpl(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    async def create(self, user: User) -> User:
        db_user = UserModel(
            email=user.email,
            name=user.name,
            hashed_password=user.hashed_password,
            role=user.role,
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return self._to_domain(db_user)

    def get_by_id(self, user_id: str) -> Optional[User]:
        db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        return self._to_domain(db_user) if db_user else None

    def get_by_email(self, email: str) -> Optional[User]:
        db_user = self.db.query(UserModel).filter(UserModel.email == email).first()
        return self._to_domain(db_user) if db_user else None

    async def get_all(self) -> List[User]:
        db_users = self.db.query(UserModel).all()
        return [self._to_domain(u) for u in db_users]

    async def update(self, user: User) -> User:
        db_user = self.db.query(UserModel).filter(UserModel.id == user.id).first()
        if db_user:
            db_user.email = user.email
            db_user.name = user.name
            db_user.role = user.role
            db_user.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(db_user)
            return self._to_domain(db_user)
        return user

    async def delete(self, user_id: str) -> bool:
        db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if db_user:
            self.db.delete(db_user)
            self.db.commit()
            return True
        return False

    def _to_domain(self, db_user: UserModel) -> User:
        return User(
            id=str(db_user.id),
            email=db_user.email,
            name=db_user.name,
            hashed_password=db_user.hashed_password,
            role=db_user.role,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at,
        )

