from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import httpx

app = FastAPI()

# Allow your Next.js frontend to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can later restrict this to your domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ODDS_API_KEY = os.environ.get("ODDS_API_KEY")

# (sport_key, league_name, sport_label)
SPORTS_TO_SHOW = [
    ("basketball_nba", "NBA", "basketball"),
    ("soccer_epl", "EPL", "soccer"),
]


@app.get("/health")
async def health():
    """
    Simple health check. Frontend uses this in the error message.
    """
    return {"status": "ok", "has_odds_key": bool(ODDS_API_KEY)}


async def fetch_games_for_sport(client: httpx.AsyncClient, sport_key: str, league: str, sport_label: str):
    """
    Call The Odds API for a single sport and massage the response into
    a simple shape that the frontend understands.
    """
    if not ODDS_API_KEY:
        raise HTTPException(status_code=500, detail="ODDS_API_KEY not set on server")

    url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds"

    params = {
        "apiKey": ODDS_API_KEY,
        "regions": "us",          # US books
        "markets": "h2h",         # moneyline only
        "oddsFormat": "american", # +110, -130, etc.
        "dateFormat": "iso",
    }

    resp = await client.get(url, params=params, timeout=10.0)
    resp.raise_for_status()
    events = resp.json()

    games = []

    for ev in events:
        home_team = ev.get("home_team")
        away_team = ev.get("away_team")
        start_time = ev.get("commence_time")
        bookmakers = ev.get("bookmakers", [])

        best_home = None
        best_away = None

        # Very simple scan: look at each bookmaker -> each market -> outcomes
        for bm in bookmakers:
            for market in bm.get("markets", []):
                if market.get("key") != "h2h":
                    continue
                for outcome in market.get("outcomes", []):
                    name = outcome.get("name")
                    price = outcome.get("price")
                    if name == home_team:
                        best_home = price if best_home is None else best_home
                    elif name == away_team:
                        best_away = price if best_away is None else best_away

        games.append(
            {
                "league": league,
                "sport": sport_label,
                "home_team": home_team,
                "away_team": away_team,
                "start_time": start_time,
                # these are just placeholders for now – you can later
                # plug in spreads/totals if you request those markets
                "market_total": None,
                "market_spread": None,
                # bonus: prices, which we can display later if you want
                "home_price": best_home,
                "away_price": best_away,
            }
        )

    return games


@app.get("/games/upcoming")
async def upcoming_games():
    """
    Option 3:
    Return today's (and upcoming) games for NBA + EPL with basic odds.
    """
    if not ODDS_API_KEY:
        raise HTTPException(status_code=500, detail="ODDS_API_KEY not set on server")

    all_games = []

    async with httpx.AsyncClient() as client:
        for sport_key, league, sport_label in SPORTS_TO_SHOW:
            try:
                games = await fetch_games_for_sport(client, sport_key, league, sport_label)
                all_games.extend(games)
            except httpx.HTTPError as e:
                # If one sport fails, log it but keep going
                print(f"Error fetching {sport_key} odds:", e)

    return all_games


@app.get("/value-picks")
async def value_picks():
    """
    For now, we aren't doing any edge calculations.
    We'll just return an empty list so the UI shows 'No picks right now'.
    Later we can compute simple 'value' based on implied probabilities.
    """
    return []
