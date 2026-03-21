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


class APITests(BaseTest):
    category = "apis"

    def run(self):
        apis = self.config.get("categories", {}).get("apis", [])

        for api in apis:
            name = api.get("name", "Unnamed API test")
            url = api.get("url", "")
            method = api.get("method", "GET").upper()
            body = api.get("body")
            expect_status = api.get("expect_status", 200)

            try:
                kwargs = {"timeout": 30, "allow_redirects": True}
                headers = {"Content-Type": "application/json"}

                if method == "POST":
                    resp, elapsed = self._timed(
                        requests.post, url,
                        json=body, headers=headers, **kwargs
                    )
                else:
                    resp, elapsed = self._timed(
                        requests.get, url, headers=headers, **kwargs
                    )

                # Capture response body (first 500 chars)
                body_text = ""
                try:
                    body_text = resp.text[:500]
                except Exception:
                    pass

                details = {
                    "url": url,
                    "method": method,
                    "status_code": resp.status_code,
                    "response_time_ms": elapsed,
                }

                # Check status
                if resp.status_code != expect_status:
                    # Build error summary
                    summary = ERROR_SUMMARIES.get(resp.status_code,
                        f"Unexpected status {resp.status_code} — expected {expect_status}.")
                    body_error = _extract_error_from_body(body_text)
                    if body_error:
                        summary = f"{summary} Server says: {body_error}"

                    details["error_summary"] = summary
                    details["response_body"] = body_text

                    self._add(name, "fail", "high",
                              f"Got {resp.status_code}, expected {expect_status}",
                              details, elapsed)
                    continue

                # Check JSON validity
                try:
                    resp.json()
                    is_json = True
                except (json.JSONDecodeError, ValueError):
                    is_json = False

                if not is_json and resp.headers.get("content-type", "").startswith("application/json"):
                    details["error_summary"] = "Response claims to be JSON but the body is not valid JSON."
                    details["response_body"] = body_text
                    self._add(name, "fail", "medium",
                              "Response claims JSON but isn't valid JSON",
                              details, elapsed)
                elif elapsed > 10000:
                    self._add(name, "warn", "medium",
                              f"Slow response: {elapsed}ms",
                              details, elapsed)
                else:
                    self._add(name, "pass", "info",
                              f"OK ({elapsed}ms)",
                              details, elapsed)

            except requests.exceptions.Timeout:
                self._add(name, "fail", "critical",
                          "Request timed out (30s)",
                          {
                              "url": url,
                              "method": method,
                              "error_summary": "Request timed out — the server took too long to respond.",
                          }, 30000)
            except requests.exceptions.ConnectionError as e:
                self._add(name, "fail", "critical",
                          f"Connection failed: {str(e)}",
                          {
                              "url": url,
                              "method": method,
                              "error_summary": "Could not connect — the server might be down.",
                          }, 0)
            except requests.exceptions.RequestException as e:
                self._add(name, "fail", "critical",
                          f"Request failed: {str(e)}",
                          {
                              "url": url,
                              "method": method,
                              "error_summary": f"Request failed: {str(e)}",
                          }, 0)

        return self.results
