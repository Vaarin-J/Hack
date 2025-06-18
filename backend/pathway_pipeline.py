import pathway as pw
from pathway import io

# Schema definitions
class KalshiSchema(pw.Schema):
    market_id: str
    question: str
    probability: float
    timestamp: str

class NewsSchema(pw.Schema):
    headline: str
    description: str
    publishedAt: str

# 1. Ingest Kalshi market data (refreshed every 60s)
kalshi_markets = io.http.read(
    url="https://kalshi-public.s3.amazonaws.com/markets.json",
    refresh_interval_ms=60000,
    schema=KalshiSchema,
    mode="replace"
)

# 2. Ingest business news (refreshed every 30s)
news_articles = io.http.read(
    url="https://newsapi.org/v2/top-headlines?category=business&apiKey=YOUR_API_KEY",
    refresh_interval_ms=30000,
    schema=NewsSchema,
    mode="replace"
)

# 3. Chunk and embed news descriptions
chunks = pw.llm.text.chunks(news_articles.description, chunk_size=200)
embeddings = pw.llm.embed.embed(chunks)

# 4. Build a vector index on the embedded chunks
vector_index = pw.llm.vector.index(embeddings, key=chunks.id)

# 5. Match Kalshi market questions to news context
retrieved_context = vector_index.find(kalshi_markets.question, top_k=3)

# 6. Generate justification using the matched context
prompt_inputs = pw.map(
    pw.this.question,
    retrieved_context.contexts,
    lambda q, ctx: f"Q: {q}\nContext:\n{ctx}\nGenerate a short rationale:"
)

rationales = pw.llm.text.generate(prompt_inputs)

# 7. Join rationales with Kalshi markets
recommendations = kalshi_markets.select(
    market_id=pw.this.market_id,
    question=pw.this.question,
    probability=pw.this.probability,
    rationale=rationales
)

# 8. Output recommendations to a local JSONL file
iosink = io.jsonlines.write(recommendations, "output/recommendations.jsonl")

# 9. Run the Pathway pipeline
pw.run()
