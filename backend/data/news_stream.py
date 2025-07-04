"""Business news stream using NewsAPI.
Requires environment variable NEWSAPI_KEY.
"""
import os
import pathway as pw
from pathway import io

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "YOUR_API_KEY")

class NewsSchema(pw.Schema):
    headline: str
    description: str
    publishedAt: str

business_news = io.http.read(
    url=f"https://newsapi.org/v2/top-headlines?category=business&apiKey={NEWSAPI_KEY}",
    refresh_interval_ms=30_000,
    schema=NewsSchema,
    mode="replace",
)