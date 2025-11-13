from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Backend running!"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/value-picks")
def value_picks():
    return [
        {
            "label": "Team A vs Team B",
            "league": "NBA",
            "book": "DraftKings",
            "edge": 0.12,
            "odds": "+150"
        },
        {
            "label": "Team C vs Team D",
            "league": "Soccer",
            "book": "FanDuel",
            "edge": 0.08,
            "odds": "+110"
        }
    ]

@app.get("/games/upcoming")
def upcoming_games():
    return [
        {
            "home_team": "Lakers",
            "away_team": "Heat",
            "league": "NBA",
            "sport": "basketball",
            "start_time": "2025-01-01T19:00:00"
        },
        {
            "home_team": "Barcelona",
            "away_team": "Real Madrid",
            "league": "La Liga",
            "sport": "soccer",
            "start_time": "2025-01-02T16:00:00"
        }
    ]
