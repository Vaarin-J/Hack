"""Economic data stream pulling CPI (Consumer Price Index) from FRED.
Requires environment variable FRED_API_KEY.
"""
import os
import pathway as pw
from pathway import io

FRED_KEY = os.getenv("FRED_API_KEY", "YOUR_FRED_KEY")

# Endpoint for CPI (All Urban Consumers) series
FRED_CPI_URL = (
    "https://api.stlouisfed.org/fred/series/observations?"
    "series_id=CPIAUCSL&api_key=" + FRED_KEY + "&file_type=json"
)

class CPISchema(pw.Schema):
    date: str  # observation date (YYYY-MM-DD)
    value: str  # CPI value as string per FRED API

# Note: response JSON is {"observations": [ ... ]}
# We use json_pointer to extract the list under "observations"
cpi_data = io.http.read(
    url=FRED_CPI_URL,
    refresh_interval_ms=86_400_000,  # daily
    schema=CPISchema,
    mode="replace",
    json_pointer="/observations",
)
