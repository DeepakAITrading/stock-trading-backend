from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
# You might need to install the smartapi-python library on your server:
# pip install smartapi-python
from SmartApi import SmartConnect 

app = FastAPI()

# This CORS middleware is essential for your frontend to connect
origins = ["*"]  # Allows all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/instruments")
async def get_instruments(request: Request):
    try:
        # 1. Get login details from the frontend's request
        login_data = await request.json()
        api_key = login_data.get('apiKey')
        client_id = login_data.get('clientId')
        password = login_data.get('password')

        # 2. Create a SmartConnect object
        obj = SmartConnect(api_key=api_key)

        # 3. Log in to Angel One to generate a session
        # Note: Angel One may require a TOTP (Time-based One-Time Password)
        # The library handles this, but you may need to provide it if enabled on your account.
        session_data = obj.generateSession(client_id, password)
        
        # Check if login was successful and we have an auth token
        if not session_data or 'data' not in session_data or 'jwtToken' not in session_data['data']:
            raise Exception("Login to Angel One failed. Check credentials.")

        # 4. Fetch the instrument list from the official URL
        instrument_url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
        response = requests.get(instrument_url)
        response.raise_for_status()  # Raises an exception for bad responses (4xx or 5xx)
        
        full_instrument_list = response.json()

        # 5. Filter for only NSE Equity stocks
        nse_equity_list = [
            {"symbol": item["symbol"], "name": item["name"]} 
            for item in full_instrument_list 
            if item.get("exch_seg") == "NSE" and item.get("symbol", "").endswith("-EQ")
        ]

        # 6. Return the filtered list to the frontend
        return nse_equity_list

    except Exception as e:
        # Return a specific error message if anything goes wrong
        return {"error": str(e)}
