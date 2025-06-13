from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import MACD

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TradeData(BaseModel):
    prices: List[float]

@app.get("/")
def read_root():
    return {"message": "Backend is live!"}

@app.post("/predict")
def predict_direction(data: TradeData):
    prices = data.prices

    if len(prices) < 26:
        return {"error": "Please send at least 26 price values."}

    df = pd.DataFrame(prices, columns=["close"])
    df["rsi"] = RSIIndicator(close=df["close"]).rsi()
    df["macd"] = MACD(close=df["close"]).macd()
    df.dropna(inplace=True)

    if df.empty:
        return {"error": "Not enough data for prediction."}

    rsi = df["rsi"].iloc[-1]
    macd = df["macd"].iloc[-1]

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
