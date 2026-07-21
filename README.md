# PokéMap Quest Route Builder

A quality-of-life web tool for Pokémon GO players. Select a city, pick today's quest rewards you're hunting, and download an optimized GPX walking route — no more zigzagging across town.

**Live at:** [pokemap.duckdns.org](https://pokemap.duckdns.org)

---

## What it does

- Pulls **live quest data** from community-run Pokémon GO maps for 5 cities
- Lets you filter by any reward available *today* (coins, stardust, items, Pokémon encounters, mega energy) — filters update automatically as events change
- Shows all matching PokéStops on an interactive dark map
- Groups quests by task condition so you can focus on one type at a time
- Generates **optimized GPX route files** (nearest-neighbor algorithm) so your walk is as efficient as possible
- Resets automatically at midnight and at 11 AM local city time (1 hour after events typically start)

## Cities supported

| City | Map source |
|------|-----------|
| 🇸🇬 Singapore | sgpokemap.com |
| 🇦🇺 Sydney | sydneypogomap.com |
| 🇬🇧 London | londonpogomap.com |
| 🇺🇸 New York City | nycpokemap.com |
| 🇨🇦 Vancouver | vanpokemap.com |

## Credits

Quest data is sourced from these community-maintained Pokémon GO maps:

- **[SGPokéMap](https://sgpokemap.com)** — Singapore
- **[Sydney Pokémon GO Map](https://sydneypogomap.com)** — Sydney
- **[London Pokémon GO Map](https://londonpogomap.com)** — London
- **[NYC PokéMap](https://nycpokemap.com)** — New York City
- **[Vancouver PokéMap](https://vanpokemap.com)** — Vancouver

Pokémon sprites provided by **[PokeAPI](https://pokeapi.co)** (open source, [PokeAPI/sprites](https://github.com/PokeAPI/sprites)).

Pokémon GO is a trademark of Niantic, Inc. and The Pokémon Company. This project is not affiliated with, endorsed by, or connected to Niantic or The Pokémon Company in any way.

## Disclaimer

This tool is a **personal quality-of-life project** built for the Pokémon GO community. It does not scrape, store, or redistribute any map data — it simply acts as a browser-side proxy so your device can fetch and display quest data from the community maps listed above. All quest data belongs to the respective map communities. Please support them and follow their terms of use.

No login, no accounts, no data collection.

---

## Running locally

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Open `http://localhost:8000` — the backend serves the frontend too.

### Frontend only (dev)

Open `frontend/index.html` directly in a browser. It auto-detects `file://` and points API calls to `localhost:8000`.

## Self-hosting (Oracle Cloud Free Tier)

See `deploy/setup.sh` for a full setup script targeting Ubuntu 20.04 + nginx + systemd.  
TL;DR: Python 3.8+, FastAPI, uvicorn behind nginx, free AMD Micro VM, DuckDNS for a free hostname, certbot for HTTPS.

```bash
bash deploy/setup.sh   # first-time setup
bash deploy/update.sh  # pull latest and restart
```

## Tech stack

| Layer | Tech |
|-------|------|
| Backend | Python / FastAPI |
| Proxy | httpx (async) |
| Route optimizer | Nearest-neighbor TSP heuristic (haversine distances) |
| Frontend | Vanilla JS + Leaflet.js |
| Map tiles | CartoDB Dark Matter |
| Hosting | Oracle Cloud Free Tier (AMD Micro) |
