"""
main_pipeline.py
This is the core Pathway pipeline for the Kalshi Weather Bot.
It handles:
1. Signal ingestion from the historical weather data replay
2. Dynamic knowledge base & RAG system for market rules
3. Agentic decision-making with conviction scoring
4. Simulated trade execution
"""

import os
import time
import datetime
import pathway as pw
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser

# Import from local modules
from data_replay import get_historical_forecasts
from kalshi_executor import execute_trade_signal

# Load environment variables
load_dotenv()

# Configuration
KALSHI_MARKET_TICKER = "HMAX-24JUN17-80"  # Example ticker for NYC max temp on June 17, 2024
CITY = "New York"
MARKET_THRESHOLD = 80.0  # Temperature threshold in Fahrenheit
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

# Define schemas
class WeatherData(pw.Schema):
    maxtemp_f: float
    last_updated: str
    location: str

# Signal Ingestion - Replay weather data
class WeatherDataSource(pw.io.python.ConnectorSubject):
    """Pathway ConnectorSubject yielding weather forecast dicts."""
    def __init__(self):
        super().__init__()
        self.forecasts = get_historical_forecasts()

    def run(self):
        """Stream each forecast to Pathway using next_json."""
        for forecast in self.forecasts:
            self.next_json(forecast)
            time.sleep(5)  # 5-second delay to simulate real-time streaming

# Create the weather data stream
weather_stream = pw.io.python.read(
    WeatherDataSource(),
    schema=WeatherData,
    autocommit_duration_ms=1000,
)

# Market rule context (single rule for simplicity)
MARKET_RULE_CONTEXT = (
    f"This is a Kalshi market for NYSE Daily Max Temperature. The ticker {KALSHI_MARKET_TICKER} refers to whether the maximum temperature in {CITY} on June 17, 2024 will be above {MARKET_THRESHOLD}°F. "
    f"If the max temperature is above {MARKET_THRESHOLD}°F, the YES contract will settle at $1. Otherwise, it will settle at $0."
)

# Initialize LLM
llm = ChatOpenAI(api_key=OPENAI_API_KEY, model_name="gpt-4.1")

# Agentic Decision & Conviction Scoring
@pw.udf
def decision_agent(maxtemp_f: float, last_updated: str, location: str) -> dict:
    """
    Agent that makes trading decisions based on temperature data
    
    Args:
        maxtemp_f: float containing max temperature
        last_updated: str containing last updated time
        location: str containing location
    
    Returns:
        dict: Trade signal with ticker, forecast temperature, side, 
              conviction score, explanation, and timestamp
    """
    forecast_temp = maxtemp_f
    timestamp = last_updated
    
    # Determine conviction and side based on forecast temperature vs threshold
    if forecast_temp > MARKET_THRESHOLD:
        side = "YES"
        # Higher conviction the more it exceeds threshold
        conviction = min(0.5 + (forecast_temp - MARKET_THRESHOLD) / 10, 0.99)
    else:
        side = "NO"
        # Higher conviction the further below threshold
        conviction = min(0.5 + (MARKET_THRESHOLD - forecast_temp) / 10, 0.99)
    
    # Use static market rule context
    rag_context = MARKET_RULE_CONTEXT
    
    # Create prompt template for LLM explanation
    prompt_template = PromptTemplate.from_template(
        """You are an expert weather data analyst for the Kalshi prediction markets.
        Given the following market information:
        
        {rag_context}
        
        And the following current weather data:
        - Current forecast temperature for {location}: {forecast_temp}°F
        - Market temperature threshold: {threshold}°F
        
        Explain in 1-2 sentences why taking the {side} position with a conviction of {conviction:.2f} 
        is the appropriate trading decision:
        """
    )
    
    # Generate explanation using LLM
    chain = prompt_template | llm | StrOutputParser()
    explanation = chain.invoke({
        "rag_context": rag_context,
        "location": location,
        "forecast_temp": forecast_temp,
        "threshold": MARKET_THRESHOLD,
        "side": side,
        "conviction": conviction
    })
    
    # Return trade signal
    return {
        "ticker": KALSHI_MARKET_TICKER,
        "forecast_temp": forecast_temp,
        "side": side,
        "conviction": conviction,
        "explanation": explanation,
        "timestamp": timestamp,
    }

# Apply decision agent to generate trade signals
trade_signals = weather_stream.select(
    signal=decision_agent(pw.this.maxtemp_f, pw.this.last_updated, pw.this.location)
)

# Create the final output table
final_output_table = trade_signals.select(
    ticker=pw.apply_with_type(lambda s: str(s["ticker"]), str, pw.this.signal),
    forecast_temp=pw.apply_with_type(lambda s: float(s["forecast_temp"]), float, pw.this.signal),
    side=pw.apply_with_type(lambda s: str(s["side"]), str, pw.this.signal),
    conviction=pw.apply_with_type(lambda s: float(s["conviction"]), float, pw.this.signal),
    explanation=pw.apply_with_type(lambda s: str(s["explanation"]), str, pw.this.signal),
    timestamp=pw.apply_with_type(lambda s: str(s["timestamp"]), str, pw.this.signal),
)

# Set up output connectors
# 1. Python observer connector for trade execution
class KalshiTradeObserver(pw.io.python.ConnectorObserver):
    def __init__(self):
        super().__init__()

    def on_change(self, key, row, time, is_addition):
        # Only handle insertions
        if is_addition:
            execute_trade_signal(row)

    def on_end(self):
        print("Pipeline stream ended.")

pw.io.python.write(final_output_table, KalshiTradeObserver())

# 2. JSONLines connector for visualization in Streamlit UI
pw.io.jsonlines.write(final_output_table, "./backend/live_data.jsonl")

# Run the pipeline
if __name__ == "__main__":
    print("Starting Kalshi Weather Bot pipeline...")
    print(f"Monitoring temperature for {CITY} with threshold {MARKET_THRESHOLD}°F")
    pw.run()
