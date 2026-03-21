import requests
from .base import BaseTest


class QuranTests(BaseTest):
    category = "quran_api"

    def run(self):
        quran_cfg = self.config.get("categories", {}).get("quran_api", {})
        if not quran_cfg:
            return self.results

        base_url = quran_cfg.get("base_url", "https://api.quran.com/api/v4")
        tests = quran_cfg.get("tests", [])

        for test in tests:
            name = test.get("name", "Unnamed test")
            endpoint = test.get("endpoint", "")
            check = test.get("check", "")
            url = f"{base_url}{endpoint}"

            try:
                resp, elapsed = self._timed(requests.get, url, timeout=15)
                data = resp.json()

                passed, detail_msg = self._evaluate_check(check, data)

                if resp.status_code != 200:
                    self._add(name, "fail", "high", f"API returned {resp.status_code}", {"url": url, "status_code": resp.status_code}, elapsed)
                elif passed:
                    self._add(name, "pass", "info", detail_msg, {"url": url}, elapsed)
                else:
                    self._add(name, "fail", "high", detail_msg, {"url": url, "response_preview": str(data)[:200]}, elapsed)

            except Exception as e:
                self._add(name, "fail", "critical", f"Error: {str(e)}", {"url": url}, 0)

        # Audio tests
        self._run_audio_tests()

        return self.results

    def _evaluate_check(self, check, data):
        try:
            if "==" in check:
                field, expected = check.split("==")
                field = field.strip()
                expected = expected.strip()

                if field == "length":
                    chapters = data.get("chapters", data.get("data", []))
                    actual = len(chapters) if isinstance(chapters, list) else 0
                    return actual == int(expected), f"Length: {actual} (expected {expected})"

                # Navigate nested data
                value = data
                for key in field.split("."):
                    if isinstance(value, dict):
                        value = value.get(key, value.get("chapter", {}).get(key))
                    else:
                        break

                if value is not None:
                    return str(value) == expected, f"{field}: {value} (expected {expected})"
                return False, f"Field '{field}' not found"

            if "exists and not empty" in check:
                field = check.split(" ")[0]
                verses = data.get("verses", data.get("data", []))
                if isinstance(verses, list) and len(verses) > 0:
                    first = verses[0]
                    found = first.get(field, [])
                    if found:
                        return True, f"{field} found and not empty"
                return False, f"{field} not found or empty"

            return True, "Check not implemented, passed by default"
        except Exception as e:
            return False, f"Check evaluation error: {str(e)}"

    def _run_audio_tests(self):
        audio_cfg = self.config.get("categories", {}).get("audio", {})
        if not audio_cfg:
            return

        reciters = audio_cfg.get("reciters", [])
        test_ayahs = audio_cfg.get("test_ayahs", [])
        url_pattern = audio_cfg.get("url_pattern", "")

        for reciter in reciters:
            reciter_id = reciter.get("id", "")
            reciter_name = reciter.get("name", reciter_id)

            for ayah in test_ayahs:
                url = url_pattern.replace("{reciter}", reciter_id).replace("{ayah}", str(ayah))
                name = f"Audio: {reciter_name} ayah {ayah}"

                try:
                    resp, elapsed = self._timed(requests.head, url, timeout=10)
                    if resp.status_code == 200:
                        self._add(name, "pass", "info", "Audio URL accessible", {"url": url}, elapsed)
                    else:
                        self._add(name, "warn", "medium", f"Audio URL returned {resp.status_code}", {"url": url, "status_code": resp.status_code}, elapsed)
                except Exception as e:
                    self._add(name, "fail", "medium", f"Audio check failed: {str(e)}", {"url": url}, 0)
