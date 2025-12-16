import pytest
from unittest.mock import MagicMock, AsyncMock
from app.application.services.project_service import ProjectService
from app.domain.entities.project import Project
from app.domain.value_objects.user_role import UserRole
from app.domain.value_objects.project_status import ProjectStatus


@pytest.mark.asyncio
async def test_create_project_success(mock_project_repository, sample_project):
    """Test successful project creation"""
    # Setup
    mock_project_repository.create = AsyncMock(return_value=sample_project)
    
    service = ProjectService(mock_project_repository)
    
    # Execute
    result = await service.create_project(
        title="Test Project",
        description="Test Description",
        status=ProjectStatus.ACTIVE,
        client_id="user-123"
    )
    
    # Assert
    assert result.id == sample_project.id
    assert result.title == "Test Project"
    assert result.description == "Test Description"
    assert result.status == ProjectStatus.ACTIVE
    assert result.client_id == "user-123"
    mock_project_repository.create.assert_called_once()


@pytest.mark.asyncio
async def test_create_project_without_client(mock_project_repository, sample_project):
    """Test project creation without client_id"""
    # Setup
    sample_project.client_id = None
    mock_project_repository.create = AsyncMock(return_value=sample_project)
    
    service = ProjectService(mock_project_repository)
    
    # Execute
    result = await service.create_project(
        title="Test Project",
        description="Test Description",
        status=ProjectStatus.ACTIVE,
        client_id=None
    )
    
    # Assert
    assert result.client_id is None
    mock_project_repository.create.assert_called_once()


@pytest.mark.asyncio
async def test_get_project_success(mock_project_repository, sample_project):
    """Test getting existing project"""
    # Setup
    mock_project_repository.get_by_id.return_value = sample_project
    
    service = ProjectService(mock_project_repository)
    
    # Execute
    result = await service.get_project("project-123")
    
    # Assert
    assert result is not None
    assert result.id == "project-123"
    mock_project_repository.get_by_id.assert_called_once_with("project-123")


@pytest.mark.asyncio
async def test_get_project_not_found(mock_project_repository):
    """Test getting non-existent project returns None"""
    # Setup
    mock_project_repository.get_by_id.return_value = None
    
    service = ProjectService(mock_project_repository)
    
    # Execute
    result = await service.get_project("nonexistent-id")
    
    # Assert
    assert result is None
    mock_project_repository.get_by_id.assert_called_once_with("nonexistent-id")


@pytest.mark.asyncio
async def test_get_all_projects_admin(mock_project_repository, sample_project):
    """Test admin gets all projects"""
    # Setup
    projects = [sample_project]
    mock_project_repository.get_all = AsyncMock(return_value=projects)
    
    service = ProjectService(mock_project_repository)
    
    # Execute
    result = await service.get_all_projects(UserRole.ADMIN, None)
    
    # Assert
    assert len(result) == 1
    assert result[0].id == sample_project.id
    mock_project_repository.get_all.assert_called_once()
    mock_project_repository.get_by_client_id.assert_not_called()


@pytest.mark.asyncio
async def test_get_all_projects_client(mock_project_repository, sample_project):
    """Test client gets only their projects"""
    # Setup
    projects = [sample_project]
    mock_project_repository.get_by_client_id = AsyncMock(return_value=projects)
    
    service = ProjectService(mock_project_repository)
    
    # Execute
    result = await service.get_all_projects(UserRole.CLIENT, "user-123")
    
    # Assert
    assert len(result) == 1
    assert result[0].id == sample_project.id
    mock_project_repository.get_by_client_id.assert_called_once_with("user-123")
    mock_project_repository.get_all.assert_not_called()


@pytest.mark.asyncio
async def test_get_all_projects_invalid_role(mock_project_repository):
    """Test invalid role returns empty list"""
    # Setup
    service = ProjectService(mock_project_repository)
    
    # Execute
    result = await service.get_all_projects(UserRole.CLIENT, None)
    
    # Assert
    assert result == []
    mock_project_repository.get_all.assert_not_called()
    mock_project_repository.get_by_client_id.assert_not_called()


@pytest.mark.asyncio
async def test_update_project_success(mock_project_repository, sample_project):
    """Test successful project update"""
    # Setup
    updated_project = Project(
        id=sample_project.id,
        title="Updated Title",
        description="Updated Description",
        status=ProjectStatus.COMPLETED,
        client_id="user-123"
    )
    mock_project_repository.get_by_id.return_value = sample_project
    mock_project_repository.update = AsyncMock(return_value=updated_project)
    
    service = ProjectService(mock_project_repository)
    
    # Execute
    result = await service.update_project(
        project_id="project-123",
        title="Updated Title",
        description="Updated Description",
        status=ProjectStatus.COMPLETED
    )
    
    # Assert
    assert result.title == "Updated Title"
    assert result.description == "Updated Description"
    assert result.status == ProjectStatus.COMPLETED
    mock_project_repository.get_by_id.assert_called_once_with("project-123")
    mock_project_repository.update.assert_called_once()


@pytest.mark.asyncio
async def test_update_project_partial(mock_project_repository, sample_project):
    """Test partial project update (only some fields)"""
    # Setup
    updated_project = Project(
        id=sample_project.id,
        title="Updated Title",
        description=sample_project.description,  # Not updated
        status=sample_project.status,  # Not updated
        client_id=sample_project.client_id
    )
    mock_project_repository.get_by_id.return_value = sample_project
    mock_project_repository.update = AsyncMock(return_value=updated_project)
    
    service = ProjectService(mock_project_repository)
    
    # Execute - only update title
    result = await service.update_project(
        project_id="project-123",
        title="Updated Title"
    )
    
    # Assert
    assert result.title == "Updated Title"
    assert result.description == sample_project.description  # Unchanged
    mock_project_repository.update.assert_called_once()


@pytest.mark.asyncio
async def test_update_project_not_found(mock_project_repository):
    """Test updating non-existent project returns None"""
    # Setup
    mock_project_repository.get_by_id.return_value = None
    
    service = ProjectService(mock_project_repository)
    
    # Execute
    result = await service.update_project(
        project_id="nonexistent-id",
        title="Updated Title"
    )
    
    # Assert
    assert result is None
    mock_project_repository.get_by_id.assert_called_once_with("nonexistent-id")
    mock_project_repository.update.assert_not_called()


@pytest.mark.asyncio
async def test_delete_project_success(mock_project_repository):
    """Test successful project deletion"""
    # Setup
    mock_project_repository.delete = AsyncMock(return_value=True)
    
    service = ProjectService(mock_project_repository)
    
    # Execute
    result = await service.delete_project("project-123")
    
    # Assert
    assert result is True
    mock_project_repository.delete.assert_called_once_with("project-123")


@pytest.mark.asyncio
async def test_delete_project_not_found(mock_project_repository):
    """Test deleting non-existent project returns False"""
    # Setup
    mock_project_repository.delete = AsyncMock(return_value=False)
    
    service = ProjectService(mock_project_repository)
    
    # Execute
    result = await service.delete_project("nonexistent-id")
    
    # Assert
    assert result is False
    mock_project_repository.delete.assert_called_once_with("nonexistent-id")

