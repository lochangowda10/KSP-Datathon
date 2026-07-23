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

# Mapping from email to token for the mock validate_token
EMAIL_TO_TOKEN = {
    "admin@ksp.gov.in": "admin-token",
    "officer@ksp.gov.in": "officer-token",
    "analyst@ksp.gov.in": "analyst-token",
    "viewer@ksp.gov.in": "viewer-token"
}

def test_orchestrator_basic():
    """Test basic orchestrator functionality."""
    # Test with user context (would normally come from auth decorator)
    user = authenticate_user("officer@ksp.gov.in", "officer123")
    assert user is not None

    token = EMAIL_TO_TOKEN[user["email"]]
    response = orchestrate_query(
        query="Show me theft cases in Delhi from January 2024",
        headers={"Authorization": f"Bearer {token}"}
    )

    # Should not have an error
    assert "error" not in response or response.get("error") is None
    assert "response" in response
    assert "sql_query" in response
    assert "evidence" in response
    assert "visualization" in response

    # Check response content
    assert isinstance(response["response"], str)
    assert len(response["response"]) > 0
    assert "theft" in response["response"].lower() or "Theft" in response["response"]

    # Check evidence structure
    assert "fir_numbers" in response["evidence"]
    assert "risk_scores" in response["evidence"]
    assert isinstance(response["evidence"]["fir_numbers"], list)
    assert len(response["evidence"]["fir_numbers"]) > 0
    assert all(isinstance(fir, str) and fir.startswith("FIR") for fir in response["evidence"]["fir_numbers"])

    risk_scores = response["evidence"]["risk_scores"]
    assert "overall" in risk_scores
    assert "level" in risk_scores
    assert "breakdown" in risk_scores
    assert isinstance(risk_scores["overall"], int)
    assert 0 <= risk_scores["overall"] <= 100
    assert risk_scores["level"] in ["low", "medium", "high"]

    # Check visualization structure
    assert "mapData" in response["visualization"]
    assert "chartData" in response["visualization"]
    assert "networkData" in response["visualization"]

    # Check map data
    map_data = response["visualization"]["mapData"]
    assert "type" in map_data
    assert map_data["type"] == "FeatureCollection"
    assert "features" in map_data
    assert isinstance(map_data["features"], list)
    assert len(map_data["features"]) > 0

    # Check chart data
    chart_data = response["visualization"]["chartData"]
    assert "labels" in chart_data
    assert "datasets" in chart_data
    assert isinstance(chart_data["labels"], list)
    assert len(chart_data["labels"]) > 0
    assert isinstance(chart_data["datasets"], list)
    assert len(chart_data["datasets"]) > 0

    # Check network data
    network_data = response["visualization"]["networkData"]
    assert "nodes" in network_data
    assert "edges" in network_data
    assert isinstance(network_data["nodes"], list)
    assert isinstance(network_data["edges"], list)
    assert len(network_data["nodes"]) > 0

    print("[PASS] orchestrator basic test passed")

def test_orchestrator_with_different_queries():
    """Test orchestrator with different types of queries."""
    user = authenticate_user("officer@ksp.gov.in", "officer123")
    assert user is not None
    token = EMAIL_TO_TOKEN[user["email"]]

    test_queries = [
        "Show me theft cases in Bangalore",
        "Find burglary incidents in Mumbai last week",
        "What are the robbery hotspots in Delhi?",
        "Show assault cases from yesterday",
        "Display murder statistics for the last month"
    ]

    for query in test_queries:
        response = orchestrate_query(query=query, headers={"Authorization": f"Bearer {token}"})

        # Should not have an error
        assert "error" not in response or response.get("error") is None
        assert "response" in response
        assert "evidence" in response
        assert "visualization" in response

        # Check that response mentions the crime type
        response_lower = response["response"].lower()
        # At least one of the crime types should be mentioned or it's a general response
        assert any(ct in response_lower for ct in ["theft", "burglary", "robbery", "assault", "murder"]) or "case" in response_lower

    print("[PASS] orchestrator different queries test passed")

def test_orchestrator_with_different_roles():
    """Test orchestrator with different user roles."""
    roles = [
        ("admin@ksp.gov.in", "admin123"),
        ("officer@ksp.gov.in", "officer123"),
        ("analyst@ksp.gov.in", "analyst123"),
        ("viewer@ksp.gov.in", "viewer123")
    ]

    test_query = "Show me recent crime incidents"

    for email, password in roles:
        user = authenticate_user(email, password)
        assert user is not None, f"Failed to authenticate {email}"

        token = EMAIL_TO_TOKEN[user["email"]]
        response = orchestrate_query(query=test_query, headers={"Authorization": f"Bearer {token}"})

        # Should not have an authentication error (our decorator would handle that in real use)
        # But we're testing the function directly, so we just check it returns something reasonable
        assert "response" in response
        assert isinstance(response["response"], str)
        assert len(response["response"]) > 0

        # Check that we get evidence and visualization data
        assert "evidence" in response
        assert "visualization" in response

    print("[PASS] orchestrator role-based test passed")

def test_orchestrator_consistency():
    """Test that identical queries produce consistent results."""
    user = authenticate_user("officer@ksp.gov.in", "officer123")
    assert user is not None
    token = EMAIL_TO_TOKEN[user["email"]]

    query = "Show me theft cases in Bangalore"

    # Run the same query multiple times
    responses = []
    for i in range(3):
        response = orchestrate_query(query=query, headers={"Authorization": f"Bearer {token}"})
        assert "error" not in response or response.get("error") is None
        responses.append(response)

    # The response text should be the same (deterministic based on query)
    # Note: Some randomness is intentional in our mock data, but core elements should be consistent
    first_response = responses[0]
    for response in responses[1:]:
        # Check that the main response text is the same
        assert response["response"] == first_response["response"]
        # Check that the SQL query is the same
        assert response["sql_query"] == first_response["sql_query"]
        # Check that the same crime type and location are detected
        assert response["evidence"]["crime_type_searched"] == first_response["evidence"]["crime_type_searched"]
        assert response["evidence"]["location_searched"] == first_response["evidence"]["location_searched"]

    print("[PASS] orchestrator consistency test passed")

if __name__ == "__main__":
    test_orchestrator_basic()
    test_orchestrator_with_different_queries()
    test_orchestrator_with_different_roles()
    test_orchestrator_consistency()
    print("All orchestrator tests passed!")