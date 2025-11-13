from datetime import datetime, timedelta
from fastapi import FastAPI
from pydantic import BaseModel

# 👇 THIS is what Render is looking for: a variable named "app"
app = FastAPI(title="Sports Edge API")


@app.get("/health")
def health():
    """Simple health-check endpoint."""
    return {"status": "ok", "time": datetime.utcnow().isoformat() + "Z"}


class ValuePick(BaseModel):
    game_id: int
    league: str
    market: str
    fair: float | None
    market_price: float | None
    edge: float | None
    note: str


@app.get("/games/upcoming")
def upcoming():
    """Mock list of upcoming games."""
    now = datetime.utcnow()
    return {
        "games": [
            {
                "game_id": 1,
                "league": "NBA",
                "start_time": (now + timedelta(hours=6)).isoformat() + "Z",
                "home": "Celtics",
                "away": "Heat",
                "market_total": 225.5,
                "market_spread": -3.5,
                "book_odds": {"home_ml": 1.67, "away_ml": 2.25},
            },
            {
                "game_id": 2,
                "league": "SOCCER",
                "start_time": (now + timedelta(hours=8)).isoformat() + "Z",
                "home": "Arsenal",
                "away": "Spurs",
                "market_total": None,
                "market_spread": None,
                "book_odds": {"home": 1.9, "draw": 3.6, "away": 4.0},
            },
        ]
    }


@app.get("/value-picks")
def value_picks():
    """Mock value picks calculated by our 'model'."""
    picks: list[ValuePick] = []

    picks.append(
        ValuePick(
            game_id=1,
            league="NBA",
            market="Home ML",
            fair=1.55,
            market_price=1.67,
            edge=(1.55 - 1.67) / 1.67,
            note="ELO favors home; opponent on 3-in-4",
        )
    )

    picks.append(
        ValuePick(
            game_id=2,
            league="SOCCER",
            market="Home (1)",
            fair=1.92,
            market_price=1.9,
            edge=(1.92 - 1.9) / 1.9,
            note="Home xG trend better last 5 matches",
        )
    )

    return {"picks": [p.model_dump() for p in picks]}
