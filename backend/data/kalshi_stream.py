import pathway as pw
from pathway import io

# Schema for Kalshi market metadata
class KalshiSchema(pw.Schema):
    market_id: str
    question: str
    probability: float
    timestamp: str

# Stream the public markets feed (updated roughly every minute)
kalshi_markets = io.http.read(
    url="https://kalshi-public.s3.amazonaws.com/markets.json",
    refresh_interval_ms=60_000,
    schema=KalshiSchema,
    mode="replace",
)