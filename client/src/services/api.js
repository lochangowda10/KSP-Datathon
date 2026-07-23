// Configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Check if we should use mock data (set to true for development without backend)
const USE_MOCK = true;

// Mock data for development
const mockResponse = {
  answer: "This is a mock response. In a real implementation, this would be the answer to your query about crime data.",
  sql_query: "SELECT * FROM incidents WHERE crime_type = 'theft' AND date >= '2024-01-01' AND date <= '2024-01-31'",
  evidence: {
    fir_numbers: ["FIR001", "FIR002", "FIR003"],
    risk_scores: {
      overall: 75,
      factors: [
        { factor: "Time of day (10PM-2AM)", points: 30 },
        { factor: "Proximity to transit hub", points: 25 },
        { factor: "Repeat location incidents", points: 20 }
      ]
    }
  },
  visualization: {
    mapData: {
      // Example GeoJSON structure (simplified)
      type: "FeatureCollection",
      features: [
        {
          type: "Feature",
          properties: {
            fir_number: "FIR001",
            crime_type: "theft",
            date: "2024-01-15",
            time: "22:30"
          },
          geometry: {
            type: "Point",
            coordinates: [77.5946, 12.9716] // Bangalore coordinates
          }
        }
        // More features would be here in a real implementation
      ]
    },
    chartData: {
      // Example chart data for a line chart (e.g., incidents over time)
      labels: ["Jan 1", "Jan 5", "Jan 10", "Jan 15", "Jan 20", "Jan 25", "Jan 31"],
      datasets: [{
        label: "Theft Incidents",
        data: [5, 8, 12, 7, 10, 15, 20],
        borderColor: "rgba(75, 192, 192, 1)",
        backgroundColor: "rgba(75, 192, 192, 0.2)"
      }]
    },
    networkData: {
      // Example network data for a force-directed graph
      nodes: [
        { id: "person1", label: "John Doe", group: 1 },
        { id: "person2", label: "Jane Smith", group: 1 },
        { id: "location1", label: "MG Road", group: 2 },
        { id: "incident1", label: "FIR001", group: 3 }
      ],
      edges: [
        { from: "person1", to: "location1" },
        { from: "person2", to: "location1" },
        { from: "person1", to: "incident1" },
        { from: "person2", to: "incident1" }
      ]
    }
  }
};

// Simulate network delay
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

export const sendQueryMock = async (query, language = 'en') => {
  // Simulate network delay
  await delay(1000);

  // In a real app, we might vary the response based on the query
  // For now, we return the same mock response for any query
  return mockResponse;
};

// In a real implementation, this would make an actual API call
export const sendQueryReal = async (query, language = 'en') => {
  try {
    const response = await fetch(`${API_BASE_URL}/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query, language }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error calling API:', error);
    throw error;
  }
};

// Export the mock version for development
export const sendQuery = USE_MOCK ? sendQueryMock : sendQueryReal;