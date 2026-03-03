from enum import Enum

import requests


class URLStatus(str, Enum):
    LIVE = "LIVE"
    DEAD = "DEAD"
    UNKNOWN = "UNKNOWN"
    LIKELY_HALLUCINATED = "LIKELY_HALLUCINATED"


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
}

WAYBACK_API = "https://archive.org/wayback/available"


def _get_wayback_snapshot(url: str, timeout: int = 10) -> str | None:
    """Return the Wayback Machine archive URL if a snapshot exists, else None."""
    try:
        resp = requests.get(WAYBACK_API, params={"url": url}, timeout=timeout)
        resp.raise_for_status()
        snapshot = resp.json().get("archived_snapshots", {}).get("closest", {})
        if snapshot.get("available"):
            return snapshot.get("url")
    except requests.RequestException:
        pass
    return None


def inspect(url: str, timeout: int = 10) -> dict:
    """Check URL liveness and, if dead, check Wayback Machine.

    Returns a dict with:
      - "url_status": one of "LIVE", "DEAD", "UNKNOWN", "LIKELY_HALLUCINATED"
      - "status_code": HTTP status code (int or None if connection failed)
      - "wayback_url": archive URL if found, else None (only set when DEAD)
    """
    result = {"url_status": None, "status_code": None, "wayback_url": None}

    try:
        resp = requests.head(
            url, allow_redirects=True, timeout=timeout, headers=HEADERS
        )

        # Fall back to GET for servers that reject HEAD
        if resp.status_code in (405, 403, 501):
            resp = requests.get(
                url,
                allow_redirects=True,
                timeout=timeout,
                headers=HEADERS,
                stream=True,
            )

        result["status_code"] = resp.status_code

        if resp.status_code == 200:
            result["url_status"] = URLStatus.LIVE
        elif resp.status_code == 404:
            wayback_url = _get_wayback_snapshot(url, timeout=timeout)
            if wayback_url:
                result["url_status"] = URLStatus.DEAD
                result["wayback_url"] = wayback_url
            else:
                result["url_status"] = URLStatus.LIKELY_HALLUCINATED
        else:
            result["url_status"] = URLStatus.UNKNOWN

    except requests.RequestException:
        result["url_status"] = URLStatus.UNKNOWN

    return result
