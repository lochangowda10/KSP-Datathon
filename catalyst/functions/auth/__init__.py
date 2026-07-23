"""
Authentication module for Catalyst Functions.
Handles user authentication and role-based access control.
"""

import json
from typing import Dict, List, Optional, Any
from functools import wraps

# Mock user database for demonstration
# In a real implementation, this would integrate with Catalyst Authentication service
MOCK_USERS = {
    "admin@ksp.gov.in": {
        "password": "admin123",  # In real app, use hashed passwords
        "role": "admin",
        "permissions": ["read", "write", "delete", "admin"],
        "name": "System Administrator"
    },
    "officer@ksp.gov.in": {
        "password": "officer123",
        "role": "officer",
        "permissions": ["read", "write"],
        "name": "Police Officer"
    },
    "analyst@ksp.gov.in": {
        "password": "analyst123",
        "role": "analyst",
        "permissions": ["read"],
        "name": "Crime Analyst"
    },
    "viewer@ksp.gov.in": {
        "password": "viewer123",
        "role": "viewer",
        "permissions": ["read"],
        "name": "Public Viewer"
    }
}

def authenticate_user(email: str, password: str) -> Optional[Dict[str, Any]]:
    """
    Authenticate a user with email and password.

    Args:
        email: User email address
        password: User password

    Returns:
        User dict if authentication successful, None otherwise
    """
    user = MOCK_USERS.get(email)
    if user and user["password"] == password:
        # Return user info without password
        return {
            "email": email,
            "role": user["role"],
            "permissions": user["permissions"],
            "name": user["name"]
        }
    return None

def require_auth(required_permissions: List[str] = None):
    """
    Decorator to require authentication and specific permissions.

    Args:
        required_permissions: List of permissions required to access the function
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # In a real implementation, we would extract auth token from headers
            # For this demo, we'll simulate authentication

            # This would normally come from request headers
            auth_header = kwargs.get('headers', {}).get('Authorization')
            if not auth_header:
                return {
                    "error": "Unauthorized",
                    "message": "Authentication token required",
                    "status_code": 401
                }

            # Extract token (simplified for demo)
            # In reality, we would validate JWT or session token
            if not auth_header.startswith("Bearer "):
                return {
                    "error": "Unauthorized",
                    "message": "Invalid token format",
                    "status_code": 401
                }

            token = auth_header[7:]  # Remove "Bearer " prefix

            # Validate token (mock implementation)
            user = validate_token(token)
            if not user:
                return {
                    "error": "Unauthorized",
                    "message": "Invalid or expired token",
                    "status_code": 401
                }

            # Check permissions if required
            if required_permissions:
                user_permissions = set(user.get("permissions", []))
                required_permissions_set = set(required_permissions)
                if not required_permissions_set.issubset(user_permissions):
                    return {
                        "error": "Forbidden",
                        "message": "Insufficient permissions",
                        "status_code": 403
                    }

            # Add user to kwargs for the function to use
            kwargs['current_user'] = user
            return func(*args, **kwargs)
        return wrapper
    return decorator

def validate_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Validate authentication token and return user info.
    In a real implementation, this would verify JWT signature or session.

    Args:
        token: Authentication token

    Returns:
        User dict if token is valid, None otherwise
    """
    # Mock token validation - in reality, this would verify a JWT
    # For demo purposes, we'll accept any token that matches a user email pattern
    if token in ["admin-token", "officer-token", "analyst-token", "viewer-token"]:
        # Map tokens to users
        token_to_user = {
            "admin-token": "admin@ksp.gov.in",
            "officer-token": "officer@ksp.gov.in",
            "analyst-token": "analyst@ksp.gov.in",
            "viewer-token": "viewer@ksp.gov.in"
        }
        email = token_to_user.get(token)
        if email:
            # Return user info without checking password (since we trust the token)
            user = MOCK_USERS.get(email)
            if user:
                return {
                    "email": email,
                    "role": user["role"],
                    "permissions": user["permissions"],
                    "name": user["name"]
                }

    return None

def get_user_role_permissions(role: str) -> List[str]:
    """
    Get permissions for a given role.

    Args:
        role: User role

    Returns:
        List of permissions for the role
    """
    role_permissions = {
        "admin": ["read", "write", "delete", "admin"],
        "officer": ["read", "write"],
        "analyst": ["read"],
        "viewer": ["read"]
    }
    return role_permissions.get(role, [])

def check_permission(user: Dict[str, Any], permission: str) -> bool:
    """
    Check if a user has a specific permission.

    Args:
        user: User dictionary
        permission: Permission to check

    Returns:
        True if user has permission, False otherwise
    """
    return permission in user.get("permissions", [])

# Export functions for use in other modules
__all__ = [
    "authenticate_user",
    "require_auth",
    "validate_token",
    "get_user_role_permissions",
    "check_permission"
]