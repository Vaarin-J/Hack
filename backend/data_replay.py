"""
data_replay.py
This module contains hardcoded historical forecast data for NYC on June 17, 2024.
This data will be used to simulate a real-time weather data stream for the Kalshi Weather Bot demo.
"""

# Historical forecast data points showing temperature crossing the threshold of 80°F
historical_forecasts = [
    {"maxtemp_f": 76.1, "last_updated": "2024-06-17T09:00:00Z", "location": "New York"},
    {"maxtemp_f": 78.3, "last_updated": "2024-06-17T10:00:00Z", "location": "New York"},
    {"maxtemp_f": 79.5, "last_updated": "2024-06-17T11:00:00Z", "location": "New York"},
    {"maxtemp_f": 80.2, "last_updated": "2024-06-17T12:00:00Z", "location": "New York"},  # KEY EVENT - crosses threshold
    {"maxtemp_f": 81.2, "last_updated": "2024-06-17T13:00:00Z", "location": "New York"},
    {"maxtemp_f": 81.5, "last_updated": "2024-06-17T15:00:00Z", "location": "New York"},
]

# Function to get the forecast data
def get_historical_forecasts():
    """
    Returns the hardcoded historical forecast data.
    
    Returns:
        list: A list of dictionaries containing historical temperature data.
    """
    return historical_forecasts
