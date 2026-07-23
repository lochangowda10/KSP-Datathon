"""
Orchestrator function for processing queries with authentication context.
"""

from auth import require_auth
import random
from datetime import datetime, timedelta
import json

@require_auth()
def orchestrate_query(query: str, user_context: dict = None, current_user: dict = None, **kwargs) -> dict:
    """
    Process a query with user context and return results with evidence and visualization data.

    Args:
        query: The user's question or command
        user_context: Additional context about the user (deprecated, use current_user)
        current_user: The authenticated user object from the require_auth decorator
        **kwargs: Additional arguments (used by decorators for headers, etc.)

    Returns:
        Dictionary containing response, evidence, and visualization data
    """
    # For backward compatibility, if user_context is provided but current_user is not,
    # we'll use user_context (though in new code, current_user should be used)
    user = current_user or user_context

    # If no user context provided, return error (should not happen with decorator)
    if not user:
        return {
            "error": "Unauthorized",
            "message": "Valid user context required",
            "status_code": 401
        }

    # In a real implementation, this would:
    # 1. Check permissions based on user role (already done by decorator if specified)
    # 2. Process the query through NLU to understand intent
    # 3. Query the database based on the understood intent
    # 4. Generate evidence trail (SQL queries, FIR numbers, risk factors)
    # 5. Prepare visualization data (maps, charts, network graphs)
    # 6. Return formatted response

    # Mock implementation that simulates processing a crime data query
    # Determine what type of query this is based on keywords
    query_lower = query.lower()

    # Default response values
    crime_type = "theft"  # default
    location = "Bangalore"  # default
    time_period = "last month"  # default

    # Try to extract information from the query
    if "theft" in query_lower:
        crime_type = "theft"
    elif "burglary" in query_lower or "break-in" in query_lower:
        crime_type = "burglary"
    elif "robbery" in query_lower:
        crime_type = "robbery"
    elif "assault" in query_lower:
        crime_type = "assault"
    elif "murder" in query_lower or "homicide" in query_lower:
        crime_type = "murder"

    # Extract location (simplified)
    locations = ["bangalore", "mumbai", "delhi", "hyderabad", "chennai", "kolkata", "pune"]
    for loc in locations:
        if loc in query_lower:
            location = loc.title()
            break

    # Extract time period (simplified)
    if "last week" in query_lower or "past week" in query_lower:
        time_period = "last week"
    elif "last month" in query_lower or "past month" in query_lower:
        time_period = "last month"
    elif "last year" in query_lower or "past year" in query_lower:
        time_period = "last year"
    elif "today" in query_lower:
        time_period = "today"
    elif "yesterday" in query_lower:
        time_period = "yesterday"

    # Generate deterministic but varied data based on the query
    # Use hash of query for consistent results
    query_hash = hash(query) % 1000

    # Generate number of incidents based on query hash
    num_incidents = max(1, (query_hash % 10) + 1)

    # Generate FIR numbers
    fir_numbers = [f"FIR{2024}{str(i+1).zfill(4)}" for i in range(num_incidents)]

    # Generate risk score based on factors
    risk_factors = [
        {"factor": "Time of day", "weight": 0.25},
        {"factor": "Location risk", "weight": 0.20},
        {"factor": "Repeat offenses", "weight": 0.15},
        {"factor": "Victim vulnerability", "weight": 0.15},
        {"factor": "Evidence quality", "weight": 0.10},
        {"factor": "Suspect history", "weight": 0.15}
    ]

    # Calculate risk score
    total_points = 0
    risk_breakdown = []
    for factor in risk_factors:
        # Generate a reasonable value for each factor based on query hash
        base_value = (query_hash + hash(factor["factor"])) % 100
        factor_value = base_value / 100.0  # 0 to 1
        points = factor_value * 100 * factor["weight"]
        total_points += points
        risk_breakdown.append({
            "factor": factor["factor"],
            "value": round(factor_value, 2),
            "weight": factor["weight"],
            "points": round(points, 1)
        })

    overall_risk_score = min(100, int(total_points))

    # Determine risk level
    if overall_risk_score < 30:
        risk_level = "low"
    elif overall_risk_score < 70:
        risk_level = "medium"
    else:
        risk_level = "high"

    # Generate mock SQL query that would have been executed
    sql_query = f"""
    SELECT
        fir_number,
        date_time,
        location,
        crime_type,
        description,
        reporting_officer
    FROM
        incidents
    WHERE
        crime_type = '{crime_type}'
        AND location LIKE '%{location}%'
        AND date_time >= DATE_SUB(NOW(), INTERVAL 1 MONTH)
    ORDER BY
        date_time DESC
    LIMIT {num_incidents};
    """.strip()

    # Generate visualization data

    # Map data (GeoJSON-like)
    map_data = {
        "type": "FeatureCollection",
        "features": []
    }

    # Generate map points for each incident
    base_lat, base_lng = 12.9716, 77.5946  # Bangalore coordinates
    for i, fir in enumerate(fir_numbers):
        # Spread points around the base location
        lat_offset = (random.randint(-50, 50) / 1000.0)  # ~+/-5km
        lng_offset = (random.randint(-50, 50) / 1000.0)

        feature = {
            "type": "Feature",
            "properties": {
                "fir_number": fir,
                "crime_type": crime_type,
                "date": (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"),
                "time": f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}",
                "risk_score": max(0, min(100, overall_risk_score + random.randint(-15, 15)))
            },
            "geometry": {
                "type": "Point",
                "coordinates": [
                    round(base_lng + lng_offset, 6),
                    round(base_lat + lat_offset, 6)
                ]
            }
        }
        map_data["features"].append(feature)

    # Chart data (time series)
    chart_data = {
        "labels": [],
        "datasets": [{
            "label": f"{crime_type.title()} Incidents",
            "data": [],
            "borderColor": "rgba(75, 192, 192, 1)",
            "backgroundColor": "rgba(75, 192, 192, 0.2)",
            "fill": False,
            "tension": 0.1
        }]
    }

    # Generate 7 days of data
    for i in range(7):
        date = (datetime.now() - timedelta(days=6-i)).strftime("%b %d")
        chart_data["labels"].append(date)
        # Generate some variation in the data
        base_count = max(0, (query_hash + i * 17) % 10)
        count = base_count + random.randint(0, 3)
        chart_data["datasets"][0]["data"].append(count)

    # Network data (showing connections between persons, locations, incidents)
    nodes = []
    edges = []

    # Add incident nodes
    for i, fir in enumerate(fir_numbers):
        nodes.append({
            "id": f"incident_{i}",
            "label": fir,
            "type": "incident",
            "group": 1
        })

    # Add location nodes (unique locations)
    locations_list = [location, "City Center", "Industrial Area", "Residential Zone"]
    unique_locations = list(set(locations_list))[:3]  # Limit to 3 locations
    for i, loc in enumerate(unique_locations):
        nodes.append({
            "id": f"location_{i}",
            "label": loc,
            "type": "location",
            "group": 2
        })

    # Add person nodes (suspects/victims/witnesses)
    persons = ["John Doe", "Jane Smith", "Robert Johnson", "Maria Garcia"]
    num_persons = min(len(persons), max(1, num_incidents))
    for i in range(num_persons):
        nodes.append({
            "id": f"person_{i}",
            "label": persons[i],
            "type": "person",
            "group": 3
        })

    # Create edges (connections)
    # Each incident connected to its location
    for i in range(len(fir_numbers)):
        loc_index = i % len(unique_locations)
        edges.append({
            "from": f"incident_{i}",
            "to": f"location_{loc_index}",
            "type": "occurred_at"
        })

    # Each incident connected to a person
    for i in range(len(fir_numbers)):
        person_index = i % num_persons if num_persons > 0 else 0
        edges.append({
            "from": f"incident_{i}",
            "to": f"person_{person_index}",
            "type": "involved_person"
        })

    # Some person-to-person connections (associates)
    if num_persons > 1:
        for i in range(num_persons - 1):
            edges.append({
                "from": f"person_{i}",
                "to": f"person_{i+1}",
                "type": "associate"
            })

    # Construct the final response
    response = {
        "response": f"Found {num_incidents} {crime_type} cases in {location} from the {time_period}.",
        "sql_query": sql_query,
        "evidence": {
            "fir_numbers": fir_numbers,
            "risk_scores": {
                "overall": overall_risk_score,
                "level": risk_level,
                "breakdown": risk_breakdown
            },
            "time_period": time_period,
            "location_searched": location,
            "crime_type_searched": crime_type
        },
        "visualization": {
            "mapData": map_data,
            "chartData": chart_data,
            "networkData": {
                "nodes": nodes,
                "edges": edges
            }
        }
    }

    return response