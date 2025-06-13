from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import MACD

# Define app
app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define expected input model
class TradeData(BaseModel):
    prices: list[float]

@app.post("/predict")
def predict_direction(data: TradeData):
    prices = data.prices

    if len(prices) < 26:
        return {"error": "Please send at least 26 price points."}

    # Create DataFrame from prices
    df = pd.DataFrame(prices, columns=["close"])

    # Calculate RSI
    rsi_indicator = RSIIndicator(close=df["close"])
    df["rsi"] = rsi_indicator.rsi()

    # Calculate MACD
    macd_indicator = MACD(close=df["close"])
    df["macd"] = macd_indicator.macd()

    # Drop rows with NaN values
    df.dropna(inplace=True)

    if df.empty:
        return {"error": "Not enough data for indicators after removing NaNs."}

    # Get latest indicators
    latest_rsi = df["rsi"].iloc[-1]
    latest_macd = df["macd"].iloc[-1]

    # Define logic
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
