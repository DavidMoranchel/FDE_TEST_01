import pytest
from datetime import timedelta
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    decode_access_token
)
from app.core.config import settings


def test_get_password_hash_generates_hash():
    """Test that password hash is generated"""
    password = "test_password_123"
    hashed = get_password_hash(password)
    
    assert hashed is not None
    assert isinstance(hashed, str)
    assert len(hashed) > 0
    assert hashed != password  # Should be different from plain password


def test_get_password_hash_different_salts():
    """Test that same password generates different hashes (due to salt)"""
    password = "test_password_123"
    hash1 = get_password_hash(password)
    hash2 = get_password_hash(password)
    
    # Hashes should be different due to random salt
    assert hash1 != hash2
    # But both should verify the same password
    assert verify_password(password, hash1)
    assert verify_password(password, hash2)


def test_verify_password_correct():
    """Test password verification with correct password"""
    password = "test_password_123"
    hashed = get_password_hash(password)
    
    result = verify_password(password, hashed)
    
    assert result is True


def test_verify_password_incorrect():
    """Test password verification with incorrect password"""
    password = "test_password_123"
    wrong_password = "wrong_password"
    hashed = get_password_hash(password)
    
    result = verify_password(wrong_password, hashed)
    
    assert result is False


def test_create_access_token_success():
    """Test that access token is created successfully"""
    data = {"sub": "user-123", "email": "test@example.com", "role": "client"}
    
    token = create_access_token(data)
    
    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0


def test_create_access_token_contains_data():
    """Test that token contains the provided data"""
    data = {"sub": "user-123", "email": "test@example.com", "role": "client"}
    
    token = create_access_token(data)
    decoded = decode_access_token(token)
    
    assert decoded is not None
    assert decoded["sub"] == "user-123"
    assert decoded["email"] == "test@example.com"
    assert decoded["role"] == "client"


def test_create_access_token_with_custom_expiry():
    """Test token creation with custom expiry time"""
    data = {"sub": "user-123"}
    expires_delta = timedelta(minutes=60)
    
    token = create_access_token(data, expires_delta=expires_delta)
    decoded = decode_access_token(token)
    
    assert decoded is not None
    assert "exp" in decoded


def test_create_access_token_default_expiry():
    """Test token uses default expiry from settings"""
    data = {"sub": "user-123"}
    
    token = create_access_token(data)
    decoded = decode_access_token(token)
    
    assert decoded is not None
    assert "exp" in decoded


def test_decode_access_token_success():
    """Test decoding valid access token"""
    data = {"sub": "user-123", "email": "test@example.com"}
    token = create_access_token(data)
    
    decoded = decode_access_token(token)
    
    assert decoded is not None
    assert decoded["sub"] == "user-123"
    assert decoded["email"] == "test@example.com"


def test_decode_access_token_invalid():
    """Test decoding invalid token returns None"""
    invalid_token = "invalid.token.here"
    
    result = decode_access_token(invalid_token)
    
    assert result is None


def test_decode_access_token_empty():
    """Test decoding empty token returns None"""
    result = decode_access_token("")
    
    assert result is None


def test_password_hash_and_verify_roundtrip():
    """Test complete password hash and verify cycle"""
    password = "my_secure_password_123"
    
    # Hash the password
    hashed = get_password_hash(password)
    
    # Verify it works
    assert verify_password(password, hashed) is True
    assert verify_password("wrong_password", hashed) is False


def test_token_encode_decode_roundtrip():
    """Test complete token creation and decoding cycle"""
    original_data = {
        "sub": "user-123",
        "email": "test@example.com",
        "role": "admin"
    }
    
    # Create token
    token = create_access_token(original_data)
    
    # Decode token
    decoded = decode_access_token(token)
    
    # Verify data matches
    assert decoded is not None
    assert decoded["sub"] == original_data["sub"]
    assert decoded["email"] == original_data["email"]
    assert decoded["role"] == original_data["role"]

