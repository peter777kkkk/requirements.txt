from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from typing import List
from ta.momentum import RSIIndicator
from ta.trend import MACD

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, set this to your Vercel frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input model using typing.List instead of list[]
class TradeData(BaseModel):
    prices: List[float]

@app.post("/predict")
def predict_direction(data: TradeData):
    prices = data.prices

    if len(prices) < 26:
        return {"error": "Please send at least 26 price values."}

    # Create DataFrame
    df = pd.DataFrame(prices, columns=["close"])

    # Add RSI and MACD indicators
    df["rsi"] = RSIIndicator(close=df["close"]).rsi()
    df["macd"] = MACD(close=df["close"]).macd()

    # Drop rows with NaNs
    df.dropna(inplace=True)

    if df.empty:
        return {"error": "Not enough data for predictions after processing."}

    latest_rsi = df["rsi"].iloc[-1]
    latest_macd = df["macd"].iloc[-1]

    # Basic prediction logic
    if latest_rsi < 30 and latest_macd > 0:
        decision = "BUY"
    elif latest_rsi > 70 and latest_macd < 0:
        decision = "SELL"
    else:
        decision = "HOLD"

    return {
        "rsi": round(float(latest_rsi), 2),
        "macd": round(float(latest_macd), 4),
        "direction": decision
    }
