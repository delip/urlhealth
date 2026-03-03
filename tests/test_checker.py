from unittest.mock import MagicMock, patch

import requests

from urlhealth import URLStatus, inspect


def _mock_response(status_code):
    resp = MagicMock()
    resp.status_code = status_code
    return resp


@patch("urlhealth.checker.requests.head")
def test_live_url(mock_head):
    mock_head.return_value = _mock_response(200)
    result = inspect("https://example.com")
    assert result["url_status"] == URLStatus.LIVE
    assert result["status_code"] == 200
    assert result["wayback_url"] is None


@patch("urlhealth.checker._get_wayback_snapshot", return_value="https://web.archive.org/web/20240101/https://example.com")
@patch("urlhealth.checker.requests.head")
def test_dead_url_with_wayback(mock_head, mock_wayback):
    mock_head.return_value = _mock_response(404)
    result = inspect("https://example.com/gone")
    assert result["url_status"] == URLStatus.DEAD
    assert result["status_code"] == 404
    assert result["wayback_url"] == "https://web.archive.org/web/20240101/https://example.com"


@patch("urlhealth.checker._get_wayback_snapshot", return_value=None)
@patch("urlhealth.checker.requests.head")
def test_likely_hallucinated(mock_head, mock_wayback):
    mock_head.return_value = _mock_response(404)
    result = inspect("https://example.com/never-existed")
    assert result["url_status"] == URLStatus.LIKELY_HALLUCINATED
    assert result["status_code"] == 404
    assert result["wayback_url"] is None


@patch("urlhealth.checker.requests.head")
def test_unknown_status(mock_head):
    mock_head.return_value = _mock_response(500)
    result = inspect("https://example.com")
    assert result["url_status"] == URLStatus.UNKNOWN
    assert result["status_code"] == 500


@patch("urlhealth.checker.requests.head", side_effect=requests.ConnectionError)
def test_connection_error(mock_head):
    result = inspect("https://example.com")
    assert result["url_status"] == URLStatus.UNKNOWN
    assert result["status_code"] is None


@patch("urlhealth.checker.requests.get")
@patch("urlhealth.checker.requests.head")
def test_head_rejected_falls_back_to_get(mock_head, mock_get):
    for code in (405, 403, 501):
        mock_head.return_value = _mock_response(code)
        mock_get.return_value = _mock_response(200)
        result = inspect("https://example.com")
        assert result["url_status"] == URLStatus.LIVE
        assert result["status_code"] == 200
        mock_get.assert_called()


@patch("urlhealth.checker.requests.get", side_effect=requests.RequestException)
@patch("urlhealth.checker.requests.head")
def test_wayback_api_error_returns_hallucinated(mock_head, mock_wb_get):
    mock_head.return_value = _mock_response(404)
    result = inspect("https://example.com/gone")
    assert result["url_status"] == URLStatus.LIKELY_HALLUCINATED
    assert result["wayback_url"] is None


def test_url_status_is_string_enum():
    assert URLStatus.LIVE == "LIVE"
    assert URLStatus.DEAD == "DEAD"
    assert isinstance(URLStatus.UNKNOWN, str)


def test_public_api_exports():
    import urlhealth
    assert hasattr(urlhealth, "inspect")
    assert hasattr(urlhealth, "URLStatus")
    assert urlhealth.__all__ == ["inspect", "URLStatus"]
