from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.infrastructure.database import get_db
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.adapters.api.v1.dependencies import get_current_user
from app.domain.entities.user import User
from app.domain.value_objects.user_role import UserRole

router = APIRouter()


class ClientResponse(BaseModel):
    id: str
    name: str
    email: str

    class Config:
        from_attributes = True


@router.get("/clients", response_model=List[ClientResponse])
async def get_clients(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get list of all clients. Admin only."""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can view clients"
        )
    
    user_repo: UserRepository = UserRepositoryImpl(db)
    all_users = await user_repo.get_all()
    clients = [u for u in all_users if u.role == UserRole.CLIENT]
    
    return [
        ClientResponse(id=client.id, name=client.name, email=client.email)
        for client in clients
    ]

