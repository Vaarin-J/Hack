# 🌡️ Kalshi Weather Trading Bot

A real-time, autonomous trading bot for Kalshi prediction markets that uses weather data to make trading decisions. Built with Pathway, LangChain, and Streamlit.

## 📝 Project Overview

This project implements a real-time trading bot for Kalshi prediction markets using a "Signal-First" Hybrid Architecture. For demo purposes, it uses a historical replay of NYC weather data for a resolved temperature market ("HMAX-24JUN17-80" - whether NYC's max temperature on June 17, 2024 will exceed 80°F).

### Core Architecture Components

1. **Real-Time Signal Ingestion (Senses)**: Replays historical weather data as a stream.
2. **Dynamic Knowledge Base & RAG (Memory)**: Uses Pathway Tables and vector indexes for market rules.
3. **Agentic Decision & Conviction Scoring (Brain)**: Employs Pathway UDFs with LLM for trading logic and explanations.
4. **Automated Trade Execution (Hands)**: Simulates Kalshi order placement based on conviction scores.

## 🛠️ Setup

### Prerequisites

- Python 3.9+
- Virtual environment (recommended)

### API Keys

This project requires the following API keys (set in the `.env` file):

- `WEATHER_API_KEY`: For WeatherAPI.com (not used in demo replay mode)
- `KALSHI_API_MEMBER_ID` and `KALSHI_API_SECRET_KEY`: For Kalshi API (not used in simulation mode)
- `OPENAI_API_KEY`: For LLM reasoning

### Installation

1. Clone the repository (if not already done)
2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Configure your API keys in the `.env` file

## 🚀 Running the Bot

### 1. Start the Pathway Pipeline

In one terminal:

```bash
python backend/main_pipeline.py
```

This will start the real-time data processing pipeline that:
- Ingests the simulated weather data
- Makes trading decisions with LLM-generated explanations
- Outputs signals to the console and JSON file

### 2. Launch the Streamlit UI

In another terminal:

```bash
streamlit run backend/ui.py
```

This will open a browser window with the real-time trading dashboard.

## 📊 System Components

### `data_replay.py`
Contains hardcoded historical weather data points for the demo, including the key event where temperature crosses the threshold.

### `kalshi_executor.py`
Handles simulated trade execution based on the conviction scores from the decision agent.

### `main_pipeline.py`
The core Pathway pipeline that processes data, makes decisions, and outputs trading signals.

### `ui.py`
Streamlit UI that visualizes the trading decisions, forecast data, and agent reasoning.

## 📋 Demo Script

The demo showcases how the trading bot reacts to changing temperature forecasts in real-time:

1. Initially, the forecast is below the 80°F threshold and the bot recommends a "NO" position
2. As the temperature forecast increases and approaches the threshold, the conviction score changes
3. When the temperature crosses 80°F, the bot switches to a "YES" position with high conviction
4. The LLM generates explanations for each decision based on the market context

## 🔗 References

- Based on Pathway's real-time AI application framework: https://github.com/pathwaycom/llm-app
- Kalshi prediction markets: https://kalshi.com/