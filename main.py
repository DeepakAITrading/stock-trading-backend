from fastapi import FastAPI, HTTPException
from smartapi import SmartConnect

# ✅ Hardcoded credentials (only use for personal/test use)
API_KEY = "8BZDjBnt"
CLIENT_ID = "deepakprabhu.28517@gmail.com"     # 🔁 Replace with your actual client ID
PASSWORD = "Deepak$1995"       # 🔁 Replace with your actual password

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "API is live and working!"}

@app.post("/instruments")
def get_instruments():
    try:
        obj = SmartConnect(api_key=API_KEY)
        data = obj.generateSession(CLIENT_ID, PASSWORD)
        token = data['data']['jwtToken']

        # Optional: set access token
        # obj.setAccessToken(token)

        instruments = obj.getInstruments(exchange='NSE')
        equity_symbols = [{"symbol": i["symbol"]} for i in instruments if i["symbol"].isalpha()]

        return equity_symbols[:300]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
