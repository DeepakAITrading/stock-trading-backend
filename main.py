from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

session_token = None
instrument_list = [
    {"symbol": "TATAMOTORS"},
    {"symbol": "RELIANCE"},
    {"symbol": "INFY"},
    {"symbol": "HDFCBANK"},
    {"symbol": "ICICIBANK"},
]

API_KEY = "8BZDjBnt"  # ⛔ Replace this with your actual API key

HEADERS = {
    "Content-Type": "application/json",
    "X-UserType": "USER",
    "X-SourceID": "WEB",
    "X-ClientLocalIP": "127.0.0.1",
    "X-ClientPublicIP": "127.0.0.1",
    "X-MACAddress": "00:00:00:00:00:00",
    "X-PrivateKey": API_KEY
}

class LoginData(BaseModel):
    client_code: str
    password: str
    totp: str

@app.post("/login")
def login_user(data: LoginData):
    global session_token
    payload = {
        "clientcode": data.client_code,
        "password": data.password,
        "totp": data.totp
    }
    res = requests.post(
        "https://apiconnect.angelbroking.com/rest/auth/angelbroking/user/v1/loginByPassword",
        json=payload,
        headers=HEADERS
    )
    if res.ok:
        session_token = res.json()["data"]["jwtToken"]
        return {"success": True}
    return {"success": False, "error": res.text}

@app.get("/instruments")
def get_instruments():
    return instrument_list

@app.get("/quote/{symbol}")
def get_quote(symbol: str):
    if not session_token:
        return {"error": "Not logged in"}
    quote_headers = HEADERS.copy()
    quote_headers["Authorization"] = f"Bearer {session_token}"
    payload = {
        "mode": "LTP",
        "exchangeTokens": {"NSE": [symbol]}
    }
    res = requests.post(
        "https://apiconnect.angelbroking.com/rest/marketdata/instruments/v1/quote",
        json=payload,
        headers=quote_headers
    )
    if res.ok:
        return res.json()["data"]["fetched"][0]
    return {"error": res.text}
