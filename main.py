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

# ✅ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, use your actual frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Root route to stop 404 at `/`
@app.get("/")
def read_root():
    return {"message": "Backend is working!"}

# ✅ Define input format
class LoginData(BaseModel):
    username: str
    password: str

# ✅ Login endpoint
@app.post("/login")
def login(data: LoginData):
    if users.get(data.username) == data.password:
        return {"message": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid credentials")
