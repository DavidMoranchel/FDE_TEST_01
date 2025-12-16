import pytest
from unittest.mock import AsyncMock
from app.application.services.comment_service import CommentService


@pytest.mark.asyncio
async def test_create_comment_success(mock_comment_repository, sample_comment):
    """Test successful comment creation"""
    # Setup
    mock_comment_repository.create = AsyncMock(return_value=sample_comment)
    
    service = CommentService(mock_comment_repository)
    
    # Execute
    result = await service.create_comment(
        project_id="project-123",
        user_id="user-123",
        content="Test comment"
    )
    
    # Assert
    assert result.id == sample_comment.id
    assert result.project_id == "project-123"
    assert result.user_id == "user-123"
    assert result.content == "Test comment"
    mock_comment_repository.create.assert_called_once()


@pytest.mark.asyncio
async def test_get_comments_by_project_success(mock_comment_repository, sample_comment):
    """Test getting comments for a project"""
    # Setup
    comments = [sample_comment]
    mock_comment_repository.get_by_project_id = AsyncMock(return_value=comments)
    
    service = CommentService(mock_comment_repository)
    
    # Execute
    result = await service.get_comments_by_project("project-123")
    
    # Assert
    assert len(result) == 1
    assert result[0].id == sample_comment.id
    assert result[0].project_id == "project-123"
    mock_comment_repository.get_by_project_id.assert_called_once_with("project-123")


@pytest.mark.asyncio
async def test_get_comments_by_project_empty(mock_comment_repository):
    """Test getting comments for project with no comments"""
    # Setup
    mock_comment_repository.get_by_project_id = AsyncMock(return_value=[])
    
    service = CommentService(mock_comment_repository)
    
    # Execute
    result = await service.get_comments_by_project("project-123")
    
    # Assert
    assert result == []
    assert len(result) == 0
    mock_comment_repository.get_by_project_id.assert_called_once_with("project-123")

