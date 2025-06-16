from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import websockets
import json

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change this to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Users stored locally
users = {
    "admin": "1234",
    "testuser": "demo"
}

# Login data format
class LoginData(BaseModel):
    username: str
    password: str

# Deriv token (your real or demo token)
DERIV_TOKEN = "FzWNtYDjEMDROSp"  # Replace this with the correct one
DERIV_WS = "wss://ws.deriv.com/websockets/v3"

# Connect to Deriv API and get balance
async def get_deriv_balance():
    try:
        async with websockets.connect(DERIV_WS) as ws:
            await ws.send(json.dumps({ "authorize": DERIV_TOKEN }))
            auth_response = await ws.recv()

            # Get balance after auth
            await ws.send(json.dumps({ "balance": 1 }))
            balance_response = await ws.recv()

            return json.loads(balance_response)
    except Exception as e:
        return {"error": str(e)}

# /login endpoint
@app.post("/login")
async def login(data: LoginData):
    if users.get(data.username) == data.password:
        balance_data = await get_deriv_balance()
        return {
            "message": "Login successful",
            "deriv_balance": balance_data
        }
    raise HTTPException(status_code=401, detail="Invalid credentials")
