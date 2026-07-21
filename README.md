# PokéMap Quest Route Builder

Live quest map and GPX route generator for Pokémon GO across 5 cities.

## Cities supported
- 🇸🇬 Singapore — sgpokemap.com
- 🇦🇺 Sydney — sydneypogomap.com
- 🇬🇧 London — londonpogomap.com
- 🇺🇸 NYC — nycpokemap.com
- 🇨🇦 Vancouver — vanpokemap.com

## Features
- Live quest data fetched directly from each city's map
- Filter by reward type (coins, lucky egg, stardust, encounters)
- Interactive Leaflet map with quest pins
- Download optimized GPX route files by condition group

## Setup

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
Open `frontend/index.html` in a browser (with backend running).

## Deploy
See Railway or Render for one-click Python deployment.
