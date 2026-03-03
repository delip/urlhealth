# urlhealth
<p align="center">
<img width="850" height="720" alt="image" src="https://github.com/user-attachments/assets/c0115221-9e1d-472f-a663-08748d2335ef" />
</p>

A Python library to check whether a URL is live, dead, or likely hallucinated. When a URL is dead, it automatically checks the [Wayback Machine](https://web.archive.org/) for an archived snapshot.

## Installation

```bash
pip install urlhealth
```

### Dependencies

- [requests](https://pypi.org/project/requests/)

## Usage

```python
from urlhealth import inspect, URLStatus

result = inspect("https://example.com")
print(result["url_status"])   # URLStatus.LIVE, .DEAD, .UNKNOWN, or .LIKELY_HALLUCINATED
print(result["status_code"])  # HTTP status code (int or None)
print(result["wayback_url"])  # Wayback Machine archive URL (str or None)
```

### Return value

`inspect(url, timeout=10)` returns a dict with three keys:

| Key | Type | Description |
|---|---|---|
| `url_status` | `URLStatus` | `LIVE` (200), `DEAD` (404 with Wayback snapshot), `LIKELY_HALLUCINATED` (404 without snapshot), or `UNKNOWN` (other status / connection error) |
| `status_code` | `int \| None` | HTTP status code, or `None` if the request failed |
| `wayback_url` | `str \| None` | Archive URL when status is `DEAD`, otherwise `None` |

### URLStatus enum

```python
class URLStatus(str, Enum):
    LIVE = "LIVE"
    DEAD = "DEAD"
    UNKNOWN = "UNKNOWN"
    LIKELY_HALLUCINATED = "LIKELY_HALLUCINATED"
```

Since `URLStatus` is a `str` enum, you can compare directly with strings:

```python
if result["url_status"] == "LIVE":
    print("URL is reachable")
```

## How it works

1. Sends an HTTP `HEAD` request to the URL (falls back to `GET` if the server returns 405, 403, or 501).
2. If the response is **200**, the URL is `LIVE`.
3. If the response is **404**, queries the Wayback Machine API:
   - Archived snapshot found &rarr; `DEAD` (with `wayback_url` populated).
   - No snapshot &rarr; `LIKELY_HALLUCINATED`.
4. Any other status code or connection error &rarr; `UNKNOWN`.

## License

See [LICENSE](LICENSE) for details.
