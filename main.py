from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# ... other imports

app = FastAPI()

# --- ADD THIS CORS MIDDLEWARE SECTION ---
origins = [
    "*"  # This allows all origins. For production, you might restrict this.
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods, including POST and OPTIONS
    allow_headers=["*"], # Allows all headers
)
# --- END OF CORS SECTION ---


# ... The rest of your app code (@app.post("/instruments"), etc.) goes here ...
