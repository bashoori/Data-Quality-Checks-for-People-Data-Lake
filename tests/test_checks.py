"""Tests for the checks, using sample data with known defects."""
import duckdb
import pytest

from qa.checks import CHECKS, run_checks
from src.pipeline import build_layers

EXPECTED_FAIL = [
    "duplicate_worker_effective_date",
    "overlapping_effective_periods",
    "end_before_start",
    "missing_hire_date",
    "missing_job_code",
    "orphan_manager",
    "sin_not_masked",
]

EXPECTED_PASS = [
    "reconciliation_row_count",
    "gold_one_row_per_worker",
]


@pytest.fixture(scope="module")
def results():
    con = duckdb.connect()
    build_layers(con)
    return {r["check"]: r for r in run_checks(con)}


@pytest.mark.parametrize("check_name", EXPECTED_FAIL)
def test_known_defect_is_detected(results, check_name):
    assert results[check_name]["status"] == "FAIL"
    assert results[check_name]["violations"] >= 1


@pytest.mark.parametrize("check_name", EXPECTED_PASS)
def test_clean_check_passes(results, check_name):
    assert results[check_name]["status"] == "PASS"


def test_every_check_is_covered(results):
    assert {c.name for c in CHECKS} == set(EXPECTED_FAIL) | set(EXPECTED_PASS)
    assert set(results) == {c.name for c in CHECKS}


def test_clean_worker_is_not_flagged(results):
    # W1002 is valid data and should not appear in overlap or duplicate violations
    con = duckdb.connect()
    build_layers(con)
    rows = con.sql(
        "SELECT * FROM (SELECT worker_id FROM silver_worker WHERE worker_id = 'W1002')"
    ).fetchall()
    assert len(rows) == 2
    assert "W1002" not in results["overlapping_effective_periods"]["sample"]
    assert "W1002" not in results["duplicate_worker_effective_date"]["sample"]
