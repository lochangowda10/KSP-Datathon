"""
Unit tests for the authentication module.
"""

import sys
import os
# Add the parent directory of the current file (which is the 'functions' directory) to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import from the auth module (which is in the functions directory)
from auth import (
    authenticate_user,
    require_auth,
    validate_token,
    get_user_role_permissions,
    check_permission
)

def test_authenticate_user():
    """Test user authentication."""
    # Test valid credentials
    user = authenticate_user("admin@ksp.gov.in", "admin123")
    assert user is not None
    assert user["email"] == "admin@ksp.gov.in"
    assert user["role"] == "admin"
    assert "admin" in user["permissions"]

    # Test invalid credentials
    user = authenticate_user("admin@ksp.gov.in", "wrongpassword")
    assert user is None

    # Test non-existent user
    user = authenticate_user("nonexistent@ksp.gov.in", "password")
    assert user is None

    print("[PASS] authenticate_user tests passed")

def test_get_user_role_permissions():
    """Test getting permissions for roles."""
    assert get_user_role_permissions("admin") == ["read", "write", "delete", "admin"]
    assert get_user_role_permissions("officer") == ["read", "write"]
    assert get_user_role_permissions("analyst") == ["read"]
    assert get_user_role_permissions("viewer") == ["read"]
    assert get_user_role_permissions("unknown") == []

    print("[PASS] get_user_role_permissions tests passed")

def test_check_permission():
    """Test permission checking."""
    user = {
        "email": "officer@ksp.gov.in",
        "role": "officer",
        "permissions": ["read", "write"]
    }

    assert check_permission(user, "read") == True
    assert check_permission(user, "write") == True
    assert check_permission(user, "delete") == False
    assert check_permission(user, "admin") == False

    print("[PASS] check_permission tests passed")

def test_validate_token():
    """Test token validation."""
    # Valid tokens
    assert validate_token("admin-token") is not None
    assert validate_token("officer-token") is not None
    assert validate_token("analyst-token") is not None
    assert validate_token("viewer-token") is not None

    # Invalid tokens
    assert validate_token("invalid-token") is None
    assert validate_token("") is None
    assert validate_token(None) is None

    print("[PASS] validate_token tests passed")

def test_require_auth_decorator():
    """Test the require_auth decorator."""
    # This is harder to test without a full request context
    # We'll test that the function exists and can be imported
    assert require_auth is not None
    assert require_auth([]) is not None

    print("[PASS] require_auth decorator tests passed")

if __name__ == "__main__":
    test_authenticate_user()
    test_get_user_role_permissions()
    test_check_permission()
    test_validate_token()
    test_require_auth_decorator()
    print("All authentication tests passed!")