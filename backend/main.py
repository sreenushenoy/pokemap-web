"""
PokéMap Quest Route Builder — FastAPI Backend
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import io, os

from cities import CITIES, REWARD_PRESETS
from proxy import fetch_quests, fetch_available_filters
from gpx import generate_gpx_zip, generate_single_gpx

app = FastAPI(title="PokéMap Route Builder API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── City & config endpoints ────────────────────────────────────────────────────

@app.get("/api/cities")
def get_cities():
    return [
        {"id": k, "name": v["name"], "flag": v["flag"]}
        for k, v in CITIES.items()
    ]


@app.get("/api/rewards")
def get_rewards():
    return [
        {"id": k, "label": v["label"], "filter": v["filter"]}
        for k, v in REWARD_PRESETS.items()
    ]


@app.get("/api/filters")
async def get_filters(city: str = Query(..., description="City code e.g. sg, syd, lon")):
    if city not in CITIES:
        raise HTTPException(404, f"Unknown city '{city}'. Valid: {list(CITIES)}")
    try:
        filters = await fetch_available_filters(city)
        return filters
    except Exception as e:
        raise HTTPException(502, f"Failed to fetch filters from {city}: {e}")


# ── Quest data endpoint ────────────────────────────────────────────────────────

@app.get("/api/quests")
async def get_quests(
    city: str = Query(..., description="City code"),
    reward: str = Query(None, description="Reward preset id e.g. coins, luckyegg"),
    filter: list[str] = Query([], description="Raw filter codes e.g. 8,10,0"),
):
    if city not in CITIES:
        raise HTTPException(404, f"Unknown city '{city}'")

    # Resolve filter codes
    filter_codes = list(filter)

    if reward:
        if reward not in REWARD_PRESETS:
            raise HTTPException(400, f"Unknown reward '{reward}'. Valid: {list(REWARD_PRESETS)}")
        preset_filter = REWARD_PRESETS[reward]["filter"]
        if preset_filter and preset_filter not in filter_codes:
            filter_codes.append(preset_filter)

    if not filter_codes:
        raise HTTPException(400, "Provide at least one filter code or a reward preset.")

    try:
        data = await fetch_quests(city, filter_codes)
    except Exception as e:
        raise HTTPException(502, f"Failed to fetch quests from {city}: {e}")

    quests = data.get("quests", [])

    # Group conditions for the UI
    conditions: dict[str, int] = {}
    for q in quests:
        cond = q.get("conditions_string", "Unknown")
        conditions[cond] = conditions.get(cond, 0) + 1

    return {
        "city": city,
        "reward": reward,
        "total": len(quests),
        "conditions": conditions,
        "quests": quests,
    }


# ── GPX download endpoints ─────────────────────────────────────────────────────

@app.get("/api/gpx/zip")
async def download_gpx_zip(
    city: str = Query(...),
    reward: str = Query(None),
    filter: list[str] = Query([]),
    top: int = Query(120, ge=10, le=500, description="Max stops per condition"),
):
    """Download a ZIP containing one optimized GPX per condition group."""
    if city not in CITIES:
        raise HTTPException(404, f"Unknown city '{city}'")

    filter_codes = list(filter)
    reward_label = "Quest"
    if reward and reward in REWARD_PRESETS:
        reward_label = REWARD_PRESETS[reward]["label"]
        preset_filter = REWARD_PRESETS[reward]["filter"]
        if preset_filter and preset_filter not in filter_codes:
            filter_codes.append(preset_filter)

    if not filter_codes:
        raise HTTPException(400, "Provide at least one filter or reward.")

    try:
        data = await fetch_quests(city, filter_codes)
    except Exception as e:
        raise HTTPException(502, str(e))

    quests = data.get("quests", [])
    if not quests:
        raise HTTPException(404, "No quests found for this filter.")

    zip_bytes = generate_gpx_zip(quests, reward_label, top)
    city_name = CITIES[city]["name"].lower()

    return StreamingResponse(
        io.BytesIO(zip_bytes),
        media_type="application/zip",
        headers={"Content-Disposition": f'attachment; filename="{city_name}_{reward or "quests"}.zip"'},
    )


@app.get("/api/gpx/single")
async def download_single_gpx(
    city: str = Query(...),
    reward: str = Query(None),
    filter: list[str] = Query([]),
    condition: str = Query(..., description="Exact condition string to generate route for"),
    top: int = Query(120, ge=10, le=500),
):
    """Download a single optimized GPX for one specific condition."""
    if city not in CITIES:
        raise HTTPException(404, f"Unknown city '{city}'")

    filter_codes = list(filter)
    reward_label = "Quest"
    if reward and reward in REWARD_PRESETS:
        reward_label = REWARD_PRESETS[reward]["label"]
        preset_filter = REWARD_PRESETS[reward]["filter"]
        if preset_filter and preset_filter not in filter_codes:
            filter_codes.append(preset_filter)

    if not filter_codes:
        raise HTTPException(400, "Provide at least one filter or reward.")

    try:
        data = await fetch_quests(city, filter_codes)
    except Exception as e:
        raise HTTPException(502, str(e))

    quests = data.get("quests", [])
    if not quests:
        raise HTTPException(404, "No quests found.")

    gpx_content = generate_single_gpx(quests, condition, reward_label, top)
    from gpx import condition_slug
    fname = f"{CITIES[city]['name'].lower()}_{condition_slug(condition)}.gpx"

    return StreamingResponse(
        io.BytesIO(gpx_content.encode("utf-8")),
        media_type="application/gpx+xml",
        headers={"Content-Disposition": f'attachment; filename="{fname}"'},
    )


# ── Serve frontend in production ───────────────────────────────────────────────

frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.isdir(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
