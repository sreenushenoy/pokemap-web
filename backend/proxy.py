"""Fetches quest data from pokemap sites, acting as a CORS proxy."""

import httpx, time, zoneinfo
from datetime import datetime, timedelta
from cities import CITIES

TIMEOUT = 20

# Cache: city -> (normalized_filters, expires_at_utc_timestamp)
_filter_cache: dict[str, tuple[list, float]] = {}


def _headers(base_url: str) -> dict:
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": f"{base_url}/quest.html",
        "X-Requested-With": "XMLHttpRequest",
    }


def _next_midnight_utc(tz_name: str) -> float:
    """UTC timestamp of next midnight in the given city timezone."""
    tz = zoneinfo.ZoneInfo(tz_name)
    tomorrow_midnight = (datetime.now(tz) + timedelta(days=1)).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    return tomorrow_midnight.timestamp()


async def fetch_quests(city: str, filter_codes: list[str]) -> dict:
    """Fetch quests from a pokemap. Returns raw API response dict."""
    cfg = CITIES[city]
    base = cfg["base_url"]
    params = [("quests[]", code) for code in filter_codes]
    params.append(("time", int(time.time() * 1000)))

    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        r = await client.get(f"{base}/quests.php", params=params, headers=_headers(base))
        r.raise_for_status()
        return r.json()


async def _learn_labels(city: str, filter_codes: list[str]) -> dict[str, str]:
    """
    Fetch real quest data for all filter codes and extract rewards_string labels.
    Batches in groups of 50 to keep URLs reasonable.
    Returns {filter_code: rewards_string}.
    """
    labels: dict[str, str] = {}
    for i in range(0, len(filter_codes), 50):
        batch = filter_codes[i : i + 50]
        try:
            data = await fetch_quests(city, batch)
        except Exception:
            continue
        for q in data.get("quests", []):
            t   = q.get("rewards_types", "")
            amt = q.get("rewards_amounts", "")
            rid = q.get("rewards_ids", "")
            code = f"{t},{amt},{rid}"
            if code and q.get("rewards_string") and code not in labels:
                labels[code] = q["rewards_string"]
    return labels


async def fetch_available_filters(city: str) -> list:
    """
    Return normalized filter groups for a city, with labels sourced from
    real quest data. Results are cached until midnight local city time.
    """
    from lookups import normalize_filters

    # Serve from cache if still valid
    now = time.time()
    if city in _filter_cache:
        cached, expires = _filter_cache[city]
        if now < expires:
            return cached

    cfg = CITIES[city]
    base = cfg["base_url"]

    # 1. Fetch raw filter list
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        r = await client.get(
            f"{base}/quests.php",
            params={"time": int(time.time() * 1000)},
            headers=_headers(base),
        )
        r.raise_for_status()
        raw_filters = r.json().get("filters", {})

    # 2. Build lookup-table labels (fast, offline)
    normalized = normalize_filters(raw_filters)

    # 3. Learn real labels from actual live quests (authoritative)
    all_codes = [opt["code"] for g in normalized for opt in g["options"]]
    real_labels = await _learn_labels(city, all_codes)

    # 4. Override with real labels wherever we learned them
    for g in normalized:
        for opt in g["options"]:
            if opt["code"] in real_labels:
                opt["label"] = real_labels[opt["code"]]

    # 5. Cache until next midnight in this city's timezone
    expires = _next_midnight_utc(cfg["tz"])
    _filter_cache[city] = (normalized, expires)

    return normalized
