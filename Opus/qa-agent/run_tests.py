#!/usr/bin/env python3
"""QA Testing Agent — run tests for any configured app and report to Supabase."""

import argparse
import os
import sys
import time
import yaml

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tests.http_tests import HTTPTests
from tests.quran_tests import QuranTests
from tests.api_tests import APITests
from tests.content_tests import ContentTests
from tests.prayer_tests import PrayerTests
from lib.supabase_client import create_run, add_result, complete_run
from lib.reporter import print_category, print_summary


TEST_CLASSES = {
    "routes": HTTPTests,
    "quran_api": QuranTests,
    "apis": APITests,
    "ai_content_review": ContentTests,
    "prayer": PrayerTests,
}


def load_config(app_name):
    config_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "config",
        f"{app_name}.yaml",
    )
    if not os.path.exists(config_path):
        print(f"Error: Config not found: {config_path}")
        sys.exit(1)

    with open(config_path) as f:
        return yaml.safe_load(f)


def main():
    parser = argparse.ArgumentParser(description="QA Testing Agent")
    parser.add_argument("--app", required=True, help="App name (matches config filename)")
    parser.add_argument("--category", help="Run only this test category")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--dry-run", action="store_true", help="Skip Supabase reporting")
    args = parser.parse_args()

    config = load_config(args.app)
    app_name = config.get("app_name", args.app)
    app_url = config.get("app_url", "")

    print(f"\n{'='*64}")
    print(f"  QA Agent — {app_name}")
    print(f"  {app_url}")
    print(f"{'='*64}")

    # Create run in Supabase
    run_id = None
    if not args.dry_run:
        try:
            run_id = create_run(app_name, app_url, "manual")
            print(f"  Run ID: {run_id}")
        except Exception as e:
            print(f"  Warning: Could not create run in Supabase: {e}")

    start_time = time.time()

    # Determine which categories to run
    categories_in_config = list(config.get("categories", {}).keys())
    if args.category:
        if args.category not in categories_in_config and args.category not in TEST_CLASSES:
            print(f"  Warning: Category '{args.category}' not in config. Available: {categories_in_config}")
            sys.exit(1)
        categories_to_run = [args.category]
    else:
        categories_to_run = categories_in_config

    all_results = []

    for cat in categories_to_run:
        test_cls = TEST_CLASSES.get(cat)
        if not test_cls:
            if args.verbose:
                print(f"\n  Skipping '{cat}' — no test class registered")
            continue

        runner = test_cls(config, verbose=args.verbose)
        results = runner.run()
        all_results.extend(results)

        # Upload results as they complete
        if run_id:
            for r in results:
                try:
                    add_result(run_id, r)
                except Exception as e:
                    if args.verbose:
                        print(f"  Warning: Could not upload result: {e}")

        print_category(cat, results)

    # Summary
    elapsed_ms = int((time.time() - start_time) * 1000)
    passed = sum(1 for r in all_results if r.status == "pass")
    failed = sum(1 for r in all_results if r.status == "fail")
    warnings = sum(1 for r in all_results if r.status == "warn")
    skipped = sum(1 for r in all_results if r.status == "skip")
    total = len(all_results)

    print_summary(total, passed, failed, warnings, skipped, elapsed_ms)

    # Complete run in Supabase
    if run_id:
        try:
            complete_run(run_id, total, passed, failed, warnings, skipped, elapsed_ms)
        except Exception as e:
            print(f"  Warning: Could not complete run in Supabase: {e}")

    # Exit code
    sys.exit(1 if failed > 0 else 0)


if __name__ == "__main__":
    main()
