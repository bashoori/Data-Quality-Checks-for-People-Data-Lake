"""نقطهٔ ورود اجرای همهٔ کنترل‌های کیفیت.

اجرا از ریشهٔ پروژه:
    python -m qa.run_all_checks
    python -m qa.run_all_checks --strict
"""
import argparse
import csv
import sys
from datetime import datetime

import duckdb

from qa.checks import run_checks
from src.config import RAW_FILE, RESULTS_DIR
from src.pipeline import build_layers


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="اجرای کنترل‌های کیفیت People Data Lake")
    parser.add_argument("--raw-file", default=str(RAW_FILE), help="مسیر فایل خروجی Workday")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="اگر حداقل یک کنترل FAIL شد، کد خروج ۱ برگردد",
    )
    args = parser.parse_args(argv)

    con = duckdb.connect()
    build_layers(con, args.raw_file)
    results = run_checks(con)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    output = RESULTS_DIR / f"qa_results_{datetime.now():%Y%m%d_%H%M%S}.csv"
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        writer.writeheader()
        writer.writerows(results)

    for r in results:
        print(f"[{r['status']}] {r['check']}: {r['violations']} violation(s)")

    failed = [r for r in results if r["status"] == "FAIL"]
    print(f"\n{len(results) - len(failed)} PASS, {len(failed)} FAIL")
    print(f"نتیجه ذخیره شد در: {output}")

    return 1 if (args.strict and failed) else 0


if __name__ == "__main__":
    sys.exit(main())
