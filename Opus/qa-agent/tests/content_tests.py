import os
import requests
from .base import BaseTest


class ContentTests(BaseTest):
    category = "ai_content_review"

    def run(self):
        ai_cfg = self.config.get("categories", {}).get("ai_content_review", {})
        if not ai_cfg or not ai_cfg.get("enabled"):
            return self.results

        api_key_env = ai_cfg.get("anthropic_api_key_env", "ANTHROPIC_API_KEY")
        api_key = os.environ.get(api_key_env)

        if not api_key:
            self._add("AI Content Review", "skip", "info",
                       f"Skipped: {api_key_env} not set")
            return self.results

        tests = ai_cfg.get("tests", [])
        for test in tests:
            name = test.get("name", "Unnamed AI test")
            test_type = test.get("type", "")

            try:
                if test_type == "tafsir_review":
                    self._run_tafsir_review(test, name, api_key)
                elif test_type == "content_review":
                    self._run_content_review(test, name, api_key)
                elif test_type == "duas_review":
                    self._run_duas_review(test, name, api_key)
                else:
                    self._add(name, "skip", "info", f"Unknown test type: {test_type}")
            except Exception as e:
                self._add(name, "fail", "medium", f"AI review error: {str(e)}")

        return self.results

    def _call_claude(self, api_key, prompt):
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text

    def _run_tafsir_review(self, test, name, api_key):
        surah = test.get("surah", 1)
        ayah = test.get("ayah", 1)
        app_url = self.config.get("app_url", "").rstrip("/")

        # Fetch tafsir from the app
        try:
            resp, elapsed = self._timed(
                requests.post,
                f"{app_url}/api/tafsir",
                json={"surah": surah, "ayah": ayah, "arabic_text": "test", "translation": "test"},
                timeout=30,
            )
            if resp.status_code != 200:
                self._add(name, "warn", "medium",
                          f"Tafsir API returned {resp.status_code}, skipping AI review",
                          {"surah": surah, "ayah": ayah}, elapsed)
                return

            tafsir_text = resp.text[:2000]
        except Exception as e:
            self._add(name, "warn", "medium", f"Could not fetch tafsir: {str(e)}")
            return

        prompt = (
            f"As an Islamic scholar, review this AI-generated tafsir for Surah {surah}, Ayah {ayah}. "
            f"Flag any errors, misattributions, or problematic statements. "
            f"Rate accuracy 1-10. Respond with ONLY the number on the first line, then explanation.\n\n"
            f"Tafsir:\n{tafsir_text}"
        )

        response, ai_elapsed = self._timed(self._call_claude, api_key, prompt)
        total_elapsed = elapsed + ai_elapsed

        try:
            score = int(response.strip().split("\n")[0].strip().split("/")[0].strip())
        except (ValueError, IndexError):
            score = 5

        details = {"surah": surah, "ayah": ayah, "score": score, "ai_feedback": response[:500]}

        if score >= 8:
            self._add(name, "pass", "info", f"AI accuracy score: {score}/10", details, total_elapsed)
        elif score >= 6:
            self._add(name, "warn", "medium", f"AI accuracy score: {score}/10", details, total_elapsed)
        else:
            self._add(name, "fail", "high", f"AI accuracy score: {score}/10", details, total_elapsed)

    def _run_content_review(self, test, name, api_key):
        content = test.get("content", [])
        prompt = (
            "Review these Islamic transliterations for accuracy and correct spelling. "
            "Rate overall accuracy 1-10. Respond with ONLY the number on the first line, then explanation.\n\n"
            f"Terms: {', '.join(content)}"
        )

        response, elapsed = self._timed(self._call_claude, api_key, prompt)

        try:
            score = int(response.strip().split("\n")[0].strip().split("/")[0].strip())
        except (ValueError, IndexError):
            score = 5

        details = {"content": content, "score": score, "ai_feedback": response[:500]}

        if score >= 8:
            self._add(name, "pass", "info", f"Content accuracy: {score}/10", details, elapsed)
        elif score >= 6:
            self._add(name, "warn", "medium", f"Content accuracy: {score}/10", details, elapsed)
        else:
            self._add(name, "fail", "high", f"Content accuracy: {score}/10", details, elapsed)

    def _run_duas_review(self, test, name, api_key):
        prompt = (
            "As an Islamic scholar, verify that the concept of 30 daily Ramadan duas is authentic and "
            "commonly practiced. Rate the authenticity of having specific duas for each day of Ramadan 1-10. "
            "Respond with ONLY the number on the first line, then explanation."
        )

        response, elapsed = self._timed(self._call_claude, api_key, prompt)

        try:
            score = int(response.strip().split("\n")[0].strip().split("/")[0].strip())
        except (ValueError, IndexError):
            score = 5

        details = {"score": score, "ai_feedback": response[:500]}

        if score >= 8:
            self._add(name, "pass", "info", f"Duas review: {score}/10", details, elapsed)
        elif score >= 6:
            self._add(name, "warn", "medium", f"Duas review: {score}/10", details, elapsed)
        else:
            self._add(name, "fail", "high", f"Duas review: {score}/10", details, elapsed)
