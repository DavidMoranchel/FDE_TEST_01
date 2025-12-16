from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.user import User


class UserRepository(ABC):
    @abstractmethod
    async def create(self, user: User) -> User:
        pass  # pragma: no cover

    @abstractmethod
    def get_by_id(self, user_id: str) -> Optional[User]:
        pass  # pragma: no cover

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        pass  # pragma: no cover

    @abstractmethod
    async def get_all(self) -> List[User]:
        pass  # pragma: no cover

    @abstractmethod
    async def update(self, user: User) -> User:
        pass  # pragma: no cover

    @abstractmethod
    async def delete(self, user_id: str) -> bool:
        pass  # pragma: no cover

