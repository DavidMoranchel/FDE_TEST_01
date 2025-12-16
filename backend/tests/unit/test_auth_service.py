import pytest
from unittest.mock import AsyncMock
from app.application.services.auth_service import AuthService
from app.domain.value_objects.user_role import UserRole
from app.core.security import get_password_hash, verify_password


@pytest.mark.asyncio
async def test_register_success(mock_user_repository, sample_user):
    """Test successful user registration"""
    # Setup
    mock_user_repository.get_by_email.return_value = None  # User doesn't exist
    mock_user_repository.create = AsyncMock(return_value=sample_user)
    
    service = AuthService(mock_user_repository)
    
    # Execute
    result = await service.register(
        email="test@example.com",
        password="password123",
        name="Test User",
        role=UserRole.CLIENT
    )
    
    # Assert
    assert "token" in result
    assert "user" in result
    assert result["user"]["email"] == "test@example.com"
    assert result["user"]["name"] == "Test User"
    assert result["user"]["role"] == "client"
    mock_user_repository.get_by_email.assert_called_once_with("test@example.com")
    mock_user_repository.create.assert_called_once()


@pytest.mark.asyncio
async def test_register_duplicate_email(mock_user_repository, sample_user):
    """Test registration with duplicate email fails"""
    # Setup
    mock_user_repository.get_by_email.return_value = sample_user  # User exists
    
    service = AuthService(mock_user_repository)
    
    # Execute & Assert
    with pytest.raises(ValueError, match="User with this email already exists"):
        await service.register(
            email="test@example.com",
            password="password123",
            name="Test User",
            role=UserRole.CLIENT
        )
    
    mock_user_repository.get_by_email.assert_called_once_with("test@example.com")
    mock_user_repository.create.assert_not_called()


@pytest.mark.asyncio
async def test_register_password_hash(mock_user_repository, sample_user):
    """Test that password is hashed during registration"""
    # Setup
    mock_user_repository.get_by_email.return_value = None
    mock_user_repository.create = AsyncMock(return_value=sample_user)
    
    service = AuthService(mock_user_repository)
    
    # Execute
    await service.register(
        email="test@example.com",
        password="password123",
        name="Test User",
        role=UserRole.CLIENT
    )
    
    # Assert - Check that create was called with hashed password
    call_args = mock_user_repository.create.call_args[0][0]
    assert call_args.hashed_password != "password123"
    assert len(call_args.hashed_password) > 0
    # Verify the hash is valid
    assert verify_password("password123", call_args.hashed_password)


@pytest.mark.asyncio
async def test_register_generates_token(mock_user_repository, sample_user):
    """Test that registration generates a valid JWT token"""
    # Setup
    mock_user_repository.get_by_email.return_value = None
    mock_user_repository.create = AsyncMock(return_value=sample_user)
    
    service = AuthService(mock_user_repository)
    
    # Execute
    result = await service.register(
        email="test@example.com",
        password="password123",
        name="Test User",
        role=UserRole.CLIENT
    )
    
    # Assert
    assert result["token"] is not None
    assert isinstance(result["token"], str)
    assert len(result["token"]) > 0


@pytest.mark.asyncio
async def test_login_success(mock_user_repository, sample_user):
    """Test successful login with valid credentials"""
    # Setup
    # Create a user with a hashed password
    hashed_password = get_password_hash("password123")
    sample_user.hashed_password = hashed_password
    mock_user_repository.get_by_email.return_value = sample_user
    
    service = AuthService(mock_user_repository)
    
    # Execute
    result = await service.login(
        email="test@example.com",
        password="password123"
    )
    
    # Assert
    assert "token" in result
    assert "user" in result
    assert result["user"]["email"] == "test@example.com"
    mock_user_repository.get_by_email.assert_called_once_with("test@example.com")


@pytest.mark.asyncio
async def test_login_invalid_email(mock_user_repository):
    """Test login with non-existent email fails"""
    # Setup
    mock_user_repository.get_by_email.return_value = None
    
    service = AuthService(mock_user_repository)
    
    # Execute & Assert
    with pytest.raises(ValueError, match="Invalid credentials"):
        await service.login(
            email="nonexistent@example.com",
            password="password123"
        )


@pytest.mark.asyncio
async def test_login_invalid_password(mock_user_repository, sample_user):
    """Test login with incorrect password fails"""
    # Setup
    hashed_password = get_password_hash("correct_password")
    sample_user.hashed_password = hashed_password
    mock_user_repository.get_by_email.return_value = sample_user
    
    service = AuthService(mock_user_repository)
    
    # Execute & Assert
    with pytest.raises(ValueError, match="Invalid credentials"):
        await service.login(
            email="test@example.com",
            password="wrong_password"
        )


@pytest.mark.asyncio
async def test_login_generates_token(mock_user_repository, sample_user):
    """Test that login generates a valid JWT token"""
    # Setup
    hashed_password = get_password_hash("password123")
    sample_user.hashed_password = hashed_password
    mock_user_repository.get_by_email.return_value = sample_user
    
    service = AuthService(mock_user_repository)
    
    # Execute
    result = await service.login(
        email="test@example.com",
        password="password123"
    )
    
    # Assert
    assert result["token"] is not None
    assert isinstance(result["token"], str)
    assert len(result["token"]) > 0

