import requests
import json
from .base import BaseTest


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

                details = {
                    "url": url,
                    "method": method,
                    "status_code": resp.status_code,
                    "response_time_ms": elapsed,
                }

                # Check status
                if resp.status_code != expect_status:
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
                          {"url": url, "method": method}, 30000)
            except requests.exceptions.RequestException as e:
                self._add(name, "fail", "critical",
                          f"Request failed: {str(e)}",
                          {"url": url, "method": method}, 0)

        return self.results
