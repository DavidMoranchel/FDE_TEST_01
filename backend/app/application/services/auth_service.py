from typing import Optional
from app.domain.entities.user import User
from app.domain.value_objects.user_role import UserRole
from app.domain.repositories.user_repository import UserRepository
from app.core.security import verify_password, get_password_hash, create_access_token
from datetime import timedelta
from app.core.config import settings


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def register(self, email: str, password: str, name: str, role: UserRole) -> dict:
        # Check if user exists
        existing_user = self.user_repository.get_by_email(email)
        if existing_user:
            raise ValueError("User with this email already exists")

        # Create new user
        hashed_password = get_password_hash(password)
        user = User(
            email=email,
            name=name,
            hashed_password=hashed_password,
            role=role,
        )
        created_user = await self.user_repository.create(user)

        # Generate token
        access_token = create_access_token(
            data={"sub": created_user.id, "email": created_user.email, "role": created_user.role.value}
        )

        return {
            "token": access_token,
            "user": {
                "id": created_user.id,
                "email": created_user.email,
                "name": created_user.name,
                "role": created_user.role.value,
            },
        }

    async def login(self, email: str, password: str) -> dict:
        user = self.user_repository.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise ValueError("Invalid credentials")

        access_token = create_access_token(
            data={"sub": user.id, "email": user.email, "role": user.role.value}
        )

        return {
            "token": access_token,
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "role": user.role.value,
            },
        }

