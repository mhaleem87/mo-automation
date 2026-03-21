from colorama import Fore, Style, init

init(autoreset=True)

ICONS = {
    "pass": f"{Fore.GREEN}\u2705 PASS{Style.RESET_ALL}",
    "fail": f"{Fore.RED}\u274c FAIL{Style.RESET_ALL}",
    "warn": f"{Fore.YELLOW}\u26a0\ufe0f  WARN{Style.RESET_ALL}",
    "skip": f"{Fore.CYAN}\u23ed\ufe0f  SKIP{Style.RESET_ALL}",
}


def print_result(result):
    icon = ICONS.get(result.status, result.status)
    line = f"  {icon}: {result.test_name}"
    if result.status in ("fail", "warn") and result.message:
        line += f" — {result.message}"
    print(line)


def print_category(category, results):
    passed = sum(1 for r in results if r.status == "pass")
    total = len(results)
    print(f"\n{Style.BRIGHT}{category}{Style.RESET_ALL} ({passed}/{total} passed)")
    print("  " + "-" * 60)
    for r in results:
        print_result(r)


def print_summary(total, passed, failed, warnings, skipped, duration_ms):
    print("\n" + "=" * 64)
    parts = []
    parts.append(f"{Fore.GREEN}{passed} passed{Style.RESET_ALL}")
    if failed:
        parts.append(f"{Fore.RED}{failed} failed{Style.RESET_ALL}")
    if warnings:
        parts.append(f"{Fore.YELLOW}{warnings} warnings{Style.RESET_ALL}")
    if skipped:
        parts.append(f"{Fore.CYAN}{skipped} skipped{Style.RESET_ALL}")

    duration = f"{duration_ms / 1000:.1f}s" if duration_ms >= 1000 else f"{duration_ms}ms"
    print(f"  {', '.join(parts)} ({duration})")
    print("=" * 64)
