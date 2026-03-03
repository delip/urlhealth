# urlhealth API Reference

## `inspect(url, timeout=10)`

Check whether a URL is live, dead, or likely hallucinated.

### Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `url` | `str` | — | The URL to check (must include scheme) |
| `timeout` | `int` | `10` | Timeout in seconds for HTTP requests |

### Return Value

Returns a `dict` with three keys:

```python
{
    "url_status": URLStatus,   # LIVE, DEAD, UNKNOWN, or LIKELY_HALLUCINATED
    "status_code": int | None, # HTTP status code, or None on connection failure
    "wayback_url": str | None  # Wayback Machine URL when status is DEAD, else None
}
```

### `URLStatus` Enum

```python
from urlhealth import URLStatus

URLStatus.LIVE                # "LIVE"
URLStatus.DEAD                # "DEAD"
URLStatus.UNKNOWN             # "UNKNOWN"
URLStatus.LIKELY_HALLUCINATED # "LIKELY_HALLUCINATED"
```

`URLStatus` is a `str` enum, so you can compare with plain strings:

```python
if result["url_status"] == "LIVE":
    print("Reachable")
```

## Algorithm

1. Send an HTTP `HEAD` request to the URL with browser-like headers.
2. If the server returns 405, 403, or 501 for HEAD, retry with `GET`.
3. Classify the response:
   - **200** → `LIVE`
   - **404** → query the Wayback Machine API (`https://archive.org/wayback/available`):
     - Snapshot found → `DEAD` (with `wayback_url` set)
     - No snapshot → `LIKELY_HALLUCINATED`
   - **Any other status** → `UNKNOWN`
4. On connection error (DNS failure, timeout, refused) → `UNKNOWN` with `status_code=None`.

## Common Issues

| Symptom | Cause | Fix |
|---|---|---|
| `UNKNOWN` for a reachable site | Site blocks HEAD and GET with non-browser headers | Not fixable via urlhealth; check manually |
| `UNKNOWN` with `status_code=None` | DNS resolution failed or connection timed out | Verify URL spelling and internet connection |
| `LIKELY_HALLUCINATED` for a real page | Page was recently removed and not yet archived | Confirm manually; Wayback Machine has a lag |
| Timeout on Wayback lookup | archive.org is slow | Increase `timeout` parameter |
| `ModuleNotFoundError` | urlhealth not installed | Run `pip install urlhealth` |
| Missing scheme error | URL lacks `http://` or `https://` | Prepend the scheme before calling `inspect()` |
