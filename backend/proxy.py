"""Fetches quest data from pokemap sites, acting as a CORS proxy."""

import httpx, time
from cities import CITIES

TIMEOUT = 15


def _headers(base_url: str) -> dict:
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": f"{base_url}/quest.html",
        "X-Requested-With": "XMLHttpRequest",
    }


async def fetch_quests(city: str, filter_codes: list[str]) -> dict:
    """
    Fetch quests from a pokemap site.
    filter_codes: list of strings like ["8,10,0", "2,1,301"]
    Returns the raw API response dict with 'quests' and 'filters' keys.
    """
    cfg = CITIES[city]
    base = cfg["base_url"]
    url = f"{base}/quests.php"

    params = [("quests[]", code) for code in filter_codes]
    params.append(("time", int(time.time() * 1000)))

    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        r = await client.get(url, params=params, headers=_headers(base))
        r.raise_for_status()
        return r.json()


async def fetch_available_filters(city: str) -> dict:
    """
    Fetch the filters object from a pokemap site (no quest filter = returns available filters only).
    Returns the 'filters' dict keyed by type (t2, t3, t7, t8, etc.)
    """
    cfg = CITIES[city]
    base = cfg["base_url"]
    url = f"{base}/quests.php"

    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        r = await client.get(url, params={"time": int(time.time() * 1000)}, headers=_headers(base))
        r.raise_for_status()
        data = r.json()
        return data.get("filters", {})
