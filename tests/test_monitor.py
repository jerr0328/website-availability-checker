import requests
from wac import monitor

SAMPLE_URL = "https://url.tld/"


def test_check_url(requests_mock):
    requests_mock.get(SAMPLE_URL, json={"success": True})
    data = monitor.check_url(SAMPLE_URL)
    assert data["url"] == SAMPLE_URL
    assert data["status_code"] == 200
    assert data["response_time"] > 0


def test_check_url_failure(requests_mock):
    requests_mock.get(SAMPLE_URL, exc=requests.exceptions.ConnectTimeout)
    data = monitor.check_url(SAMPLE_URL)
    assert data["url"] == SAMPLE_URL
    assert data["error"] == "ConnectTimeout()"
