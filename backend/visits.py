"""Simple persistent visitor counter stored in a local JSON file."""
from __future__ import annotations

import json, os, threading
from datetime import datetime, timezone

_FILE = os.path.join(os.path.dirname(__file__), "visits.json")
_lock = threading.Lock()


def _load() -> dict:
    if not os.path.exists(_FILE):
        return {"total": 0, "log": []}
    with open(_FILE) as f:
        return json.load(f)


def _save(data: dict) -> None:
    with open(_FILE, "w") as f:
        json.dump(data, f)


def record_visit() -> int:
    with _lock:
        data = _load()
        data["total"] += 1
        data["log"].append(datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M"))
        data["log"] = data["log"][-5000:]
        _save(data)
        return data["total"]


def get_count() -> int:
    with _lock:
        return _load()["total"]
