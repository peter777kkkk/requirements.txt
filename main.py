from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ✅ Define hardcoded users
users = {
    "admin": "1234",
    "testuser": "demo"
}

# ✅ Create FastAPI app
app = FastAPI()

# ✅ Enable CORS for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Define login input format
class LoginData(BaseModel):
    username: str
    password: str

# ✅ /login endpoint
@app.post("/login")
def login(data: LoginData):
    if users.get(data.username) == data.password:
        return {"message": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid credentials")
