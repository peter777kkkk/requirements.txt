from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from typing import List
from ta.momentum import RSIIndicator
from ta.trend import MACD

# Initialize FastAPI app
app = FastAPI()

# Enable CORS for all origins (adjust in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the expected input schema
class TradeData(BaseModel):
    prices: List[float]

# Simple root endpoint
@app.get("/")
def root():
    return {"message": "Backend is working!"}

# Main prediction endpoint
@app.post("/predict")
def predict_direction(data: TradeData):
    prices = data.prices

    # Ensure we have enough data
    if len(prices) < 26:
        return {"error": "Please send at least 26 price values."}

    # Create DataFrame from input prices
    df = pd.DataFrame(prices, columns=["close"])

    # Calculate indicators
    rsi_calc = RSIIndicator(close=df["close"])
    macd_calc = MACD(close=df["close"])

    df["rsi"] = rsi_calc.rsi()
    df["macd"] = macd_calc.macd()

    # Drop rows with NaN values
    df.dropna(inplace=True)

    # Handle insufficient data after dropna
    if df.empty:
        return {"error": "Not enough valid data after computing indicators."}

    # Extract the latest RSI and MACD values
    rsi = df["rsi"].iloc[-1]
    macd = df["macd"].iloc[-1]

    # Determine trade direction
    if rsi < 30 and macd > 0:
        direction = "BUY"
    elif rsi > 70 and macd < 0:
        direction = "SELL"
    else:
        direction = "HOLD"

    return {
        "rsi": round(float(rsi), 2),
        "macd": round(float(macd), 4),
        "direction": direction
    }