import requests
from .base import BaseTest


class PrayerTests(BaseTest):
    category = "prayer"

    def run(self):
        apis = self.config.get("categories", {}).get("apis", [])
        prayer_apis = [a for a in apis if "prayer" in a.get("name", "").lower()]

        if not prayer_apis:
            return self.results

        for api in prayer_apis:
            url = api.get("url", "")
            name = api.get("name", "Prayer API test")

            try:
                resp, elapsed = self._timed(requests.get, url, timeout=15)

                if resp.status_code != 200:
                    self._add(name, "fail", "high",
                              f"Prayer API returned {resp.status_code}",
                              {"url": url}, elapsed)
                    continue

                data = resp.json()
                timings = data.get("data", {}).get("timings", {})

                if not timings:
                    self._add(name, "fail", "high",
                              "No prayer timings in response",
                              {"url": url}, elapsed)
                    continue

                required = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]
                missing = [p for p in required if p not in timings]

                if missing:
                    self._add(name, "fail", "high",
                              f"Missing prayer times: {', '.join(missing)}",
                              {"url": url, "timings": timings}, elapsed)
                else:
                    self._add(name, "pass", "info",
                              f"All 5 prayer times present ({elapsed}ms)",
                              {"url": url, "timings": {k: timings[k] for k in required}}, elapsed)

            except Exception as e:
                self._add(name, "fail", "critical",
                          f"Prayer test failed: {str(e)}",
                          {"url": url}, 0)

        return self.results
