"""مسیرها و تنظیمات پروژه."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = ROOT / "data" / "raw" / "workday_worker_extract.csv"
RESULTS_DIR = ROOT / "qa" / "results"
