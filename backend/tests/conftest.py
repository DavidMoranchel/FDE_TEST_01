import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime
from app.domain.entities.user import User
from app.domain.entities.project import Project
from app.domain.entities.comment import Comment
from app.domain.value_objects.user_role import UserRole
from app.domain.value_objects.project_status import ProjectStatus
from app.domain.repositories.user_repository import UserRepository
from app.domain.repositories.project_repository import ProjectRepository
from app.domain.repositories.comment_repository import CommentRepository


@pytest.fixture
def mock_user_repository():
    """Mock UserRepository for testing"""
    mock = MagicMock(spec=UserRepository)
    mock.get_by_email = MagicMock()
    mock.get_by_id = MagicMock()
    mock.create = AsyncMock()
    mock.get_all = AsyncMock()
    mock.update = AsyncMock()
    mock.delete = AsyncMock()
    return mock


@pytest.fixture
def mock_project_repository():
    """Mock ProjectRepository for testing"""
    mock = MagicMock(spec=ProjectRepository)
    mock.create = AsyncMock()
    mock.get_by_id = MagicMock()
    mock.get_all = AsyncMock()
    mock.get_by_client_id = AsyncMock()
    mock.update = AsyncMock()
    mock.delete = AsyncMock()
    return mock


@pytest.fixture
def mock_comment_repository():
    """Mock CommentRepository for testing"""
    mock = MagicMock(spec=CommentRepository)
    mock.create = AsyncMock()
    mock.get_by_project_id = AsyncMock()
    return mock


@pytest.fixture
def sample_user():
    """Sample user for testing"""
    return User(
        id="user-123",
        email="test@example.com",
        name="Test User",
        hashed_password="hashed_password_123",
        role=UserRole.CLIENT,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )


@pytest.fixture
def sample_admin_user():
    """Sample admin user for testing"""
    return User(
        id="admin-123",
        email="admin@example.com",
        name="Admin User",
        hashed_password="hashed_password_123",
        role=UserRole.ADMIN,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )


@pytest.fixture
def sample_project():
    """Sample project for testing"""
    return Project(
        id="project-123",
        title="Test Project",
        description="Test Description",
        status=ProjectStatus.ACTIVE,
        client_id="user-123",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )


@pytest.fixture
def sample_comment():
    """Sample comment for testing"""
    return Comment(
        id="comment-123",
        project_id="project-123",
        user_id="user-123",
        content="Test comment",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

