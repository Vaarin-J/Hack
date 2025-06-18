"""Tech news stream via NewsAPI or fallback RSS.
Requires environment variable NEWSAPI_KEY.
"""
import os
import pathway as pw
from pathway import io

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "YOUR_API_KEY")

class TechNewsSchema(pw.Schema):
    headline: str
    description: str
    publishedAt: str

tech_news = io.http.read(
    url=f"https://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey={NEWSAPI_KEY}",
    refresh_interval_ms=30_000,
    schema=TechNewsSchema,
    mode="replace",
)
