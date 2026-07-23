"""
Unit tests for the analytics module.
"""

import sys
import os
# Add the parent directory of the current file (which is the 'functions' directory) to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import from the analytics module (which is in the functions directory)
from analytics import (
    detect_trends,
    calculate_risk_score,
    analyze_network,
    generate_report,
    process_natural_language,
    translate_text
)

def test_detect_trends():
    """Test trend detection."""
    # Sample data
    data = [
        {"date": "2024-01-01", "count": 5},
        {"date": "2024-01-02", "count": 7},
        {"date": "2024-01-03", "count": 10},
        {"date": "2024-01-04", "count": 8},
        {"date": "2024-01-05", "count": 12}
    ]

    result = detect_trends(data)

    assert "trend" in result
    assert "confidence" in result
    assert "forecast" in result
    assert isinstance(result["forecast"], list)

    print("PASS: detect_trends test passed")

def test_calculate_risk_score():
    """Test risk score calculation."""
    factors = [
        ("Time of day", 0.8),
        ("Location", 0.6),
        ("History", 0.9)
    ]

    result = calculate_risk_score(factors)

    assert "score" in result
    assert "breakdown" in result
    assert "risk_level" in result
    assert isinstance(result["score"], (int, float))
    assert 0 <= result["score"] <= 100

    print("PASS: calculate_risk_score test passed")

def test_analyze_network():
    """Test network analysis."""
    nodes = [
        {"id": "A", "label": "Node A"},
        {"id": "B", "label": "Node B"},
        {"id": "C", "label": "Node C"}
    ]

    edges = [
        {"source": "A", "target": "B"},
        {"source": "B", "target": "C"}
    ]

    result = analyze_network(nodes, edges)

    assert "node_count" in result
    assert "edge_count" in result
    assert "density" in result
    assert result["node_count"] == 3
    assert result["edge_count"] == 2

    print("PASS: analyze_network test passed")

def test_generate_report():
    """Test report generation."""
    data = [{"id": 1, "value": 10}, {"id": 2, "value": 20}]

    result = generate_report(data, "test")

    assert "title" in result
    assert "generated_at" in result
    assert "data_summary" in result
    assert "sections" in result

    print("PASS: generate_report test passed")

def test_process_natural_language():
    """Test NLP processing."""
    text = "Show me theft cases in Bangalore from January 2024"

    result = process_natural_language(text)

    assert "intent" in result
    assert "entities" in result
    assert "confidence" in result

    print("PASS: process_natural_language test passed")

def test_translate_text():
    """Test translation function."""
    text = "Hello world"

    result = translate_text(text, "es")  # Spanish

    assert "original" in result
    assert "translated" in result
    assert "source_language" in result
    assert "target_language" in result
    assert result["target_language"] == "es"

    print("PASS: translate_text test passed")

if __name__ == "__main__":
    test_detect_trends()
    test_calculate_risk_score()
    test_analyze_network()
    test_generate_report()
    test_process_natural_language()
    test_translate_text()
    print("All analytics tests passed!")