---
name: url-health
description: >
  Check if URLs are live, dead, or likely hallucinated using the urlhealth Python
  library. Automatically checks Wayback Machine for archived snapshots of dead URLs.
  Triggers on: "check url", "validate link", "is this link alive", "broken link",
  "dead link", "hallucinated url", "url health", "check link status", "verify url",
  "link checker", "url status", "wayback machine".
allowed-tools:
  - Bash(python3 -c *)
  - Bash(pip install urlhealth)
  - Bash(pip show urlhealth)
  - Bash(which python3)
---

# url-health — Check URL Liveness

## Prerequisites

Check if urlhealth is installed:

```bash
pip show urlhealth
```

If not found, install it:

```bash
pip install urlhealth
```

## Basic Usage — Single URL

```bash
python3 -c "
from urlhealth import inspect
result = inspect('THE_URL_HERE')
print(f\"Status: {result['url_status']}\")
print(f\"HTTP code: {result['status_code']}\")
if result['wayback_url']:
    print(f\"Wayback: {result['wayback_url']}\")
"
```

Replace `THE_URL_HERE` with the actual URL. The `inspect()` function returns a dict with three keys: `url_status`, `status_code`, and `wayback_url`.

## Batch Usage — Multiple URLs

```bash
python3 -c "
from urlhealth import inspect
urls = [
    'https://example.com',
    'https://example.com/nonexistent-page',
]
for url in urls:
    r = inspect(url)
    status = r['url_status']
    wayback = f\" (archived: {r['wayback_url']})\" if r['wayback_url'] else ''
    print(f\"{status}: {url}{wayback}\")
"
```

## Interpreting Results

| `url_status` | Meaning |
|---|---|
| `LIVE` | URL returned HTTP 200 — it's reachable |
| `DEAD` | URL returned 404, but a Wayback Machine snapshot exists (`wayback_url` is populated) |
| `LIKELY_HALLUCINATED` | URL returned 404 with no Wayback snapshot — probably never existed |
| `UNKNOWN` | Non-404 error or connection failure — cannot determine status |

## Optional Parameters

`inspect(url, timeout=10)` — the `timeout` parameter (seconds) controls both the URL check and the Wayback Machine lookup. Increase for slow servers.

## Error Handling

| Scenario | Behavior |
|---|---|
| Connection refused / DNS failure | Returns `UNKNOWN` with `status_code=None` |
| Timeout | Returns `UNKNOWN` with `status_code=None` |
| HTTP 403/405/501 on HEAD | Automatically retries with GET |
| urlhealth not installed | Install with `pip install urlhealth` |

If `inspect()` raises an unexpected exception, ensure the URL includes a scheme (`http://` or `https://`).

## Additional Resources

See [references/api-guide.md](references/api-guide.md) for detailed API documentation, return value structure, and the liveness-check algorithm.
