from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.application.services.auth_service import AuthService
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.adapters.api.v1.schemas import LoginRequest, RegisterRequest, AuthResponse
from app.domain.value_objects.user_role import UserRole

router = APIRouter()


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    user_repo: UserRepository = UserRepositoryImpl(db)
    return AuthService(user_repo)


@router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest, service: AuthService = Depends(get_auth_service)):
    try:
        result = await service.login(request.email, request.password)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post("/register", response_model=AuthResponse)
async def register(request: RegisterRequest, service: AuthService = Depends(get_auth_service)):
    try:
        result = await service.register(request.email, request.password, request.name, request.role)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

