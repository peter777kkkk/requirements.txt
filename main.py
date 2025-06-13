from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import ta  # Technical Analysis library

app = FastAPI()

# CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your Vercel domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Expected input: list of prices
class TradeData(BaseModel):
    prices: list[float]

@app.post("/predict")
def predict_direction(data: TradeData):
    prices = data.prices

    if len(prices) < 15:
        return {"error": "Send at least 15 price values"}

    # Create DataFrame
    df = pd.DataFrame(prices, columns=["close"])

    # Add indicators
    df["rsi"] = ta.momentum.RSIIndicator(df["close"]).rsi()
    df["macd"] = ta.trend.MACD(df["close"]).macd()

    latest_rsi = df["rsi"].iloc[-1]
    latest_macd = df["macd"].iloc[-1]

    # Simple logic
    if latest_rsi < 30 and latest_macd > 0:
        decision = "BUY"
    elif latest_rsi > 70 and latest_macd < 0:
        decision = "SELL"
    else:
        decision = "HOLD"

    return {
        "rsi": round(float(latest_rsi), 2),
        "macd": round(float(latest_macd), 2),
        "direction": decision
    }
