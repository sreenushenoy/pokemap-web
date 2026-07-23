"""Fetches quest data from pokemap sites, acting as a CORS proxy."""
from __future__ import annotations

import httpx, time, asyncio
try:
    import zoneinfo
except ImportError:
    from backports import zoneinfo
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


def _next_cache_expiry(tz_name: str) -> float:
    tz = zoneinfo.ZoneInfo(tz_name)
    now = datetime.now(tz)
    # Refresh at 10:10, 14:10, 17:10, 19:10 local time to catch event starts/updates
    checkpoints = [(10, 10), (14, 10), (17, 10), (19, 10)]
    candidates = [
        now.replace(hour=h, minute=m, second=0, microsecond=0)
        for h, m in checkpoints
        if now.replace(hour=h, minute=m, second=0, microsecond=0) > now
    ]
    midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    candidates.append(midnight)
    return min(candidates).timestamp()


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


async def _learn_labels(city: str, filter_codes: list[str]) -> dict[str, dict]:
    """
    Fetch real quest data for all filter codes concurrently.
    Returns {filter_code: {label, image}}.
    """
    batches = [filter_codes[i : i + 50] for i in range(0, len(filter_codes), 50)]

    async def fetch_batch(batch):
        try:
            return await fetch_quests(city, batch)
        except Exception:
            return {}

    responses = await asyncio.gather(*[fetch_batch(b) for b in batches])

    results: dict[str, dict] = {}
    for data in responses:
        for q in data.get("quests", []):
            t   = str(q.get("rewards_types", ""))
            amt = str(q.get("rewards_amounts", ""))
            rid = str(q.get("rewards_ids", ""))
            code = f"{t},{amt},{rid}"
            if code and q.get("rewards_string") and code not in results:
                label = q["rewards_string"]
                # For items/mega/encounters, strip the leading count from rewards_string
                # ("3 Ultra Balls" → "Ultra Balls") so quantity can be formatted separately.
                # Don't strip for stardust (t=3) or coins (t=8) where the number IS the value.
                if t in ("2", "7", "12") and amt:
                    prefix = f"{amt} "
                    if label.startswith(prefix):
                        label = label[len(prefix):]
                results[code] = {
                    "label": label,
                    "image": q.get("image", ""),
                }
    return results


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

    # 4. Override labels and expand quantity variants for items / mega energy
    for g in normalized:
        if g["group"] in ("items", "mega"):
            new_options = []
            for opt in g["options"]:
                t_num, _, base_id = opt["code"].split(",")
                # Find all quantity variants for this item discovered from live quests
                variants = {
                    code: info for code, info in real_labels.items()
                    if code.split(",")[0] == t_num and code.split(",")[2] == base_id
                }
                if len(variants) > 1:
                    for code in sorted(variants, key=lambda c: int(c.split(",")[1])):
                        amt = code.split(",")[1]
                        info = variants[code]
                        label = info["label"]
                        if amt not in ("0", "1"):
                            label = f"{amt}× {label}"
                        new_options.append({"code": code, "label": label, "image": info["image"]})
                elif variants:
                    code, info = next(iter(variants.items()))
                    amt = code.split(",")[1]
                    label = info["label"]
                    if amt not in ("0", "1"):
                        label = f"{amt}× {label}"
                    new_options.append({"code": code, "label": label, "image": info["image"]})
                else:
                    new_options.append(opt)
            g["options"] = sorted(new_options, key=lambda o: o["label"])
        else:
            for opt in g["options"]:
                if opt["code"] in real_labels:
                    opt["label"] = real_labels[opt["code"]]["label"]
                    opt["image"] = real_labels[opt["code"]]["image"]

    # 5. Only cache non-empty results — don't cache an empty result so the next
    # request retries rather than serving stale emptiness all day.
    if normalized:
        expires = _next_cache_expiry(cfg["tz"])
        _filter_cache[city] = (normalized, expires)

    return normalized
