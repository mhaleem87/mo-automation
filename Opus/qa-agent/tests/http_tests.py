import requests
import json
from .base import BaseTest

ERROR_SUMMARIES = {
    401: "Unauthorized — API key missing or invalid.",
    403: "Forbidden — authentication or permissions issue.",
    404: "Page not found — this route doesn't exist or was removed.",
    429: "Rate limited — too many requests. The API is throttling.",
    500: "Server error — the API crashed while processing the request. Check server logs.",
    502: "Bad gateway — the upstream server returned an invalid response.",
    503: "Service unavailable — the server is overloaded or under maintenance.",
    504: "Gateway timeout — the upstream server took too long to respond.",
}


def _extract_error_from_body(body_text):
    """Try to extract a meaningful error message from response body."""
    try:
        data = json.loads(body_text)
        for key in ("error", "message", "detail", "error_message"):
            if key in data:
                val = data[key]
                if isinstance(val, str):
                    return val
                if isinstance(val, dict) and "message" in val:
                    return val["message"]
        return None
    except (json.JSONDecodeError, ValueError):
        return None


class HTTPTests(BaseTest):
    category = "routes"

    def run(self):
        routes = self.config.get("categories", {}).get("routes", [])
        base_url = self.config.get("app_url", "").rstrip("/")

        for route in routes:
            path = route.get("path", "/")
            expect = route.get("expect_status", 200)
            url = f"{base_url}{path}"
            test_name = f"GET {path} returns {expect}"

            try:
                resp, elapsed = self._timed(requests.get, url, timeout=15, allow_redirects=True)

                # Capture response body (first 500 chars)
                body_text = ""
                try:
                    body_text = resp.text[:500]
                except Exception:
                    pass

                details = {
                    "url": url,
                    "status_code": resp.status_code,
                    "response_time_ms": elapsed,
                }

                if resp.status_code != expect:
                    summary = ERROR_SUMMARIES.get(resp.status_code,
                        f"Unexpected status {resp.status_code} — expected {expect}.")
                    body_error = _extract_error_from_body(body_text)
                    if body_error:
                        summary = f"{summary} Server says: {body_error}"

                    details["error_summary"] = summary
                    details["response_body"] = body_text

                    self._add(test_name, "fail", "high",
                              f"Got {resp.status_code}, expected {expect}",
                              details, elapsed)
                elif elapsed > 10000:
                    self._add(test_name, "fail", "medium",
                              f"Response took {elapsed}ms (>10s)",
                              details, elapsed)
                elif elapsed > 3000:
                    self._add(test_name, "warn", "low",
                              f"Slow response: {elapsed}ms (>3s)",
                              details, elapsed)
                else:
                    self._add(test_name, "pass", "info",
                              f"OK ({elapsed}ms)",
                              details, elapsed)

            except requests.exceptions.Timeout:
                self._add(test_name, "fail", "critical",
                          "Request timed out (15s)",
                          {
                              "url": url,
                              "error_summary": "Request timed out — the server took too long to respond.",
                          }, 15000)
            except requests.exceptions.ConnectionError as e:
                self._add(test_name, "fail", "critical",
                          f"Connection failed: {str(e)}",
                          {
                              "url": url,
                              "error_summary": "Could not connect — the server might be down.",
                          }, 0)
            except requests.exceptions.RequestException as e:
                self._add(test_name, "fail", "critical",
                          f"Request failed: {str(e)}",
                          {
                              "url": url,
                              "error_summary": f"Request failed: {str(e)}",
                          }, 0)

        return self.results
