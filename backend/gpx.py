"""Route optimization and GPX file generation."""
from __future__ import annotations

import math, io, zipfile, re


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    return R * 2 * math.asin(math.sqrt(a))


def _lat(s) -> float:
    return float(s["lat"])


def _lng(s) -> float:
    return float(s["lng"])


def nearest_neighbor(pts: list) -> list:
    if not pts:
        return pts
    unvisited = list(range(len(pts)))
    start = min(unvisited, key=lambda i: _lat(pts[i]))
    route = [start]
    unvisited.remove(start)
    while unvisited:
        last = route[-1]
        nearest = min(
            unvisited,
            key=lambda i: haversine(_lat(pts[last]), _lng(pts[last]), _lat(pts[i]), _lng(pts[i])),
        )
        route.append(nearest)
        unvisited.remove(nearest)
    return [pts[i] for i in route]


def pick_nearest_to_centroid(stops: list, n: int) -> list:
    if len(stops) <= n:
        return stops
    clat = sum(_lat(s) for s in stops) / len(stops)
    clon = sum(_lng(s) for s in stops) / len(stops)
    return sorted(stops, key=lambda s: haversine(clat, clon, _lat(s), _lng(s)))[:n]


def condition_slug(cond: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", cond.lower()).strip("_")
    return slug[:40]


def _escape(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build_gpx(title: str, waypoints: list) -> str:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<gpx version="1.1" creator="PokéMap Route Builder" xmlns="http://www.topografix.com/GPX/1/1">',
        f"  <metadata><name>{_escape(title)}</name></metadata>",
    ]
    for w in waypoints:
        lines.append(
            f'  <wpt lat="{_lat(w)}" lon="{_lng(w)}">'
            f'<name>{_escape(w["name"])}</name>'
            f'<desc>{_escape(w.get("conditions_string", ""))}</desc>'
            f"</wpt>"
        )
    lines.append("</gpx>")
    return "\n".join(lines)


def generate_gpx_zip(quests: list, reward_label: str, top: int) -> bytes:
    """
    Groups quests by conditions_string, picks top N nearest stops per group,
    optimizes each route, and returns a zip file containing one GPX per group.
    """
    # Group by condition
    groups: dict[str, list] = {}
    for q in quests:
        cond = q.get("conditions_string", "Unknown")
        groups.setdefault(cond, []).append(q)

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for cond, stops in groups.items():
            selected = pick_nearest_to_centroid(stops, top)
            optimized = nearest_neighbor(selected)
            title = f"{reward_label} — {cond}"
            gpx_content = build_gpx(title, optimized)
            fname = f"{condition_slug(cond)}.gpx"
            zf.writestr(fname, gpx_content)

    return buf.getvalue()


def generate_single_gpx(quests: list, condition: str, reward_label: str, top: int) -> str:
    """Generate a single GPX for one specific condition string."""
    filtered = [q for q in quests if q.get("conditions_string") == condition]
    selected = pick_nearest_to_centroid(filtered, top)
    optimized = nearest_neighbor(selected)
    return build_gpx(f"{reward_label} — {condition}", optimized)
