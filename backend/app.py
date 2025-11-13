from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend (localhost + vercel)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/value-picks")
def value_picks():
    return [
        {
            "label": "Test Pick",
            "league": "NBA",
            "book": "DraftKings",
            "edge": 0.12,
            "odds": "+150",
        }
    ]

@app.get("/games/upcoming")
def upcoming_games():
    return [
        {
            "home_team": "Lakers",
            "away_team": "Warriors",
            "league": "NBA",
            "sport": "basketball",
            "start_time": "2025-11-13T20:00:00Z",
            "market_total": 225.5,
            "market_spread": -3.5,
        }
    ]
