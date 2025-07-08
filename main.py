from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from smartapi import SmartConnect

import os

app = FastAPI()

class LoginRequest(BaseModel):
    clientId: str
    password: str
    apiKey: str

@app.post("/instruments")
def get_instruments(req: LoginRequest):
    try:
        obj = SmartConnect(api_key=req.apiKey)
        data = obj.generateSession(req.clientId, req.password)
        token = data['data']['jwtToken']

        # Save session token if needed
        # obj.setAccessToken(token)

        instruments = obj.getInstruments(exchange='NSE')
        equity_symbols = [{"symbol": i["symbol"]} for i in instruments if i["symbol"].isalpha()]

        return equity_symbols[:300]  # Return first 300 to avoid overloading frontend
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
