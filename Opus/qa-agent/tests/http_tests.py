import requests
from .base import BaseTest


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
                details = {
                    "url": url,
                    "status_code": resp.status_code,
                    "response_time_ms": elapsed,
                }

                if resp.status_code != expect:
                    self._add(test_name, "fail", "high", f"Got {resp.status_code}, expected {expect}", details, elapsed)
                elif elapsed > 10000:
                    self._add(test_name, "fail", "medium", f"Response took {elapsed}ms (>10s)", details, elapsed)
                elif elapsed > 3000:
                    self._add(test_name, "warn", "low", f"Slow response: {elapsed}ms (>3s)", details, elapsed)
                else:
                    self._add(test_name, "pass", "info", f"OK ({elapsed}ms)", details, elapsed)

            except requests.exceptions.Timeout:
                self._add(test_name, "fail", "critical", "Request timed out (15s)", {"url": url}, 15000)
            except requests.exceptions.RequestException as e:
                self._add(test_name, "fail", "critical", f"Request failed: {str(e)}", {"url": url}, 0)

        return self.results
