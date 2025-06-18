"""Political news stream via NewsAPI.
Requires environment variable NEWSAPI_KEY.
"""
import os
import pathway as pw
from pathway import io

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "YOUR_API_KEY")

class PoliticalNewsSchema(pw.Schema):
    headline: str
    description: str
    publishedAt: str

political_news = io.http.read(
    url=f"https://newsapi.org/v2/top-headlines?category=politics&apiKey={NEWSAPI_KEY}",
    refresh_interval_ms=30_000,
    schema=PoliticalNewsSchema,
    mode="replace",
)
