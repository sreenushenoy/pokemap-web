"""
PokéMap Quest Route Builder — FastAPI Backend
"""
from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
import io, os

from cities import CITIES
from proxy import fetch_quests, fetch_available_filters
from gpx import generate_gpx_zip, generate_single_gpx, condition_slug
from visits import record_visit, get_count

app = FastAPI(title="PokéMap Route Builder API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def _require_city(city: str):
    if city not in CITIES:
        raise HTTPException(404, f"Unknown city '{city}'. Valid: {list(CITIES)}")


def _require_filters(filter_codes: list[str]):
    if not filter_codes:
        raise HTTPException(400, "Provide at least one filter[] code.")


# ── Visitor counter ────────────────────────────────────────────────────────────

@app.post("/api/visit")
def log_visit():
    return {"count": record_visit()}

@app.get("/api/visits")
def visit_count():
    return {"count": get_count()}


# ── Config endpoints ───────────────────────────────────────────────────────────

@app.get("/api/cities")
def get_cities():
    return [
        {"id": k, "name": v["name"], "flag": v["flag"], "tz": v["tz"]}
        for k, v in CITIES.items()
    ]


@app.get("/api/filters")
async def get_filters(city: str = Query(...)):
    _require_city(city)
    try:
        return await fetch_available_filters(city)
    except Exception as e:
        raise HTTPException(502, f"Failed to fetch filters from {city}: {e}")


# ── Quest data ─────────────────────────────────────────────────────────────────

@app.get("/api/quests")
async def get_quests(
    city: str = Query(...),
    filter: list[str] = Query([], description="Filter codes, e.g. filter=8,10,0&filter=3,500,0"),
    label: str = Query("Quest", description="Human-readable reward label for GPX titles"),
):
    _require_city(city)
    _require_filters(filter)

    try:
        data = await fetch_quests(city, list(filter))
    except Exception as e:
        raise HTTPException(502, f"Failed to fetch quests from {city}: {e}")

    quests = data.get("quests", [])

    conditions: dict[str, int] = {}
    for q in quests:
        cond = q.get("conditions_string", "Unknown")
        conditions[cond] = conditions.get(cond, 0) + 1

    return {
        "city": city,
        "total": len(quests),
        "conditions": conditions,
        "quests": quests,
    }


# ── GPX downloads ──────────────────────────────────────────────────────────────

@app.get("/api/gpx/zip")
async def download_gpx_zip(
    city: str = Query(...),
    filter: list[str] = Query([]),
    label: str = Query("Quest"),
    top: int = Query(120, ge=10, le=500),
):
    """ZIP of one optimized GPX per condition group."""
    _require_city(city)
    _require_filters(filter)

    try:
        data = await fetch_quests(city, list(filter))
    except Exception as e:
        raise HTTPException(502, str(e))

    quests = data.get("quests", [])
    if not quests:
        raise HTTPException(404, "No quests found for this filter.")

    zip_bytes = generate_gpx_zip(quests, label, top)
    city_name = CITIES[city]["name"].lower()
    slug = condition_slug(label)

    return StreamingResponse(
        io.BytesIO(zip_bytes),
        media_type="application/zip",
        headers={"Content-Disposition": f'attachment; filename="{city_name}_{slug}.zip"'},
    )


@app.get("/api/gpx/single")
async def download_single_gpx(
    city: str = Query(...),
    filter: list[str] = Query([]),
    label: str = Query("Quest"),
    condition: str = Query(...),
    top: int = Query(120, ge=10, le=500),
):
    """Single optimized GPX for one condition."""
    _require_city(city)
    _require_filters(filter)

    try:
        data = await fetch_quests(city, list(filter))
    except Exception as e:
        raise HTTPException(502, str(e))

    quests = data.get("quests", [])
    if not quests:
        raise HTTPException(404, "No quests found.")

    gpx_content = generate_single_gpx(quests, condition, label, top)
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
