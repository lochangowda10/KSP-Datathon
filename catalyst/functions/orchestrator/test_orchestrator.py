"""
Tests for orchestrator function.
"""

import sys
import os
# Add the parent directory of the current file (which is the 'functions' directory) to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import from the auth and orchestrator modules
from auth import authenticate_user
from orchestrator import orchestrate_query

def test_orchestrator_basic():
    """Test basic orchestrator functionality."""
    # Test without authentication (should work for backward compatibility in basic mode)
    # Note: Our current decorator requires auth, so we'll need to handle this in the test
    # For now, we'll test with a mock user context

    # Test with user context
    user = authenticate_user("officer@ksp.gov.in", "officer123")
    assert user is not None

    response = orchestrate_query(
        query="Show me theft cases in Delhi from January 2024",
        user_context=user
    )

    assert "error" not in response
    assert "response" in response
    assert "sql_query" in response
    assert "evidence" in response
    assert "visualization" in response

    # Check evidence structure
    assert "fir_numbers" in response["evidence"]
    assert "risk_scores" in response["evidence"]
    assert isinstance(response["evidence"]["fir_numbers"], list)
    assert len(response["evidence"]["fir_numbers"]) > 0

    # Check visualization structure
    assert "mapData" in response["visualization"]
    assert "chartData" in response["visualization"]
    assert "networkData" in response["visualization"]

    print("✓ orchestrator basic test passed")

def test_orchestrator_with_different_roles():
    """Test orchestrator with different user roles."""
    roles = [
        ("admin@ksp.gov.in", "admin123"),
        ("officer@ksp.gov.in", "officer123"),
        ("analyst@ksp.gov.in", "analyst123"),
        ("viewer@ksp.gov.in", "viewer123")
    ]

    for email, password in roles:
        user = authenticate_user(email, password)
        assert user is not None, f"Failed to authenticate {email}"

        response = orchestrate_query(
            query="Test query",
            user_context=user
        )

        assert "error" not in response, f"Error for {email}: {response.get('error')}"
        assert "response" in response
        assert "visualization" in response

    print("✓ orchestrator role-based test passed")

def test_orchestrator_error_handling():
    """Test orchestrator error handling."""
    # Test with invalid user (no permissions - though our mock doesn't enforce this yet)
    # For now, we'll just verify it doesn't crash

    response = orchestrate_query(
        query="Test query",
        user_context={}  # Empty user context
    )

    # Should still return a response (our mock doesn't validate user heavily)
    assert "response" in response

    print("✓ orchestrator error handling test passed")

if __name__ == "__main__":
    test_orchestrator_basic()
    test_orchestrator_with_different_roles()
    test_orchestrator_error_handling()
    print("All orchestrator tests passed!")