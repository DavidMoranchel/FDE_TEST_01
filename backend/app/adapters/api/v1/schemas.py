from pydantic import BaseModel, EmailStr
from typing import Optional
from app.domain.value_objects.user_role import UserRole
from app.domain.value_objects.project_status import ProjectStatus


# Auth schemas
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: str
    role: UserRole


class AuthResponse(BaseModel):
    token: str
    user: dict


# Project schemas
class ProjectCreate(BaseModel):
    title: str
    description: str
    status: ProjectStatus = ProjectStatus.ACTIVE
    client_id: Optional[str] = None


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None
    client_id: Optional[str] = None


class ProjectResponse(BaseModel):
    id: str
    title: str
    description: str
    status: str
    client_id: Optional[str] = None
    client_name: Optional[str] = None
    created_at: str
    updated_at: str


# Comment schemas
class CommentCreate(BaseModel):
    content: str


class CommentResponse(BaseModel):
    id: str
    project_id: str
    user_id: str
    user_name: str
    content: str
    created_at: str
    updated_at: str

