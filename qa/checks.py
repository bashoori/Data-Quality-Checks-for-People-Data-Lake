"""Data quality checks for the People Data Lake layers.

Each check has a query that returns the rows that violate it.
If the query returns no rows, the check is PASS.
"""
from dataclasses import dataclass

import duckdb


@dataclass(frozen=True)
class Check:
    name: str
    description: str
    violations_sql: str


CHECKS: list[Check] = [
    Check(
        name="reconciliation_row_count",
        description="Bronze and Silver must have the same number of rows",
        violations_sql="""
            SELECT b.n AS bronze_rows, s.n AS silver_rows
            FROM (SELECT COUNT(*) AS n FROM bronze_workday) b,
                 (SELECT COUNT(*) AS n FROM silver_worker) s
            WHERE b.n <> s.n
        """,
    ),
    Check(
        name="duplicate_worker_effective_date",
        description="A worker must not have more than one record for the same effective date",
        violations_sql="""
            SELECT worker_id, effective_date, COUNT(*) AS occurrences
            FROM silver_worker
            GROUP BY worker_id, effective_date
            HAVING COUNT(*) > 1
        """,
    ),
    Check(
        name="overlapping_effective_periods",
        description="A worker's effective periods must not overlap",
        violations_sql="""
            SELECT a.worker_id,
                   a.effective_date,
                   a.end_date,
                   b.effective_date AS overlapping_start
            FROM silver_worker a
            JOIN silver_worker b
              ON a.worker_id = b.worker_id
             AND a.effective_date < b.effective_date
             AND a.end_date >= b.effective_date
        """,
    ),
    Check(
        name="end_before_start",
        description="End date must not be earlier than the start date",
        violations_sql="""
            SELECT worker_id, effective_date, end_date
            FROM silver_worker
            WHERE end_date < effective_date
        """,
    ),
    Check(
        name="missing_hire_date",
        description="Hire date must not be empty",
        violations_sql="""
            SELECT worker_id, effective_date
            FROM silver_worker
            WHERE hire_date IS NULL
        """,
    ),
    Check(
        name="missing_job_code",
        description="Job code must not be empty",
        violations_sql="""
            SELECT worker_id, effective_date
            FROM silver_worker
            WHERE job_code IS NULL
        """,
    ),
    Check(
        name="orphan_manager",
        description="The manager ID must exist as a worker in the file",
        violations_sql="""
            SELECT worker_id, manager_id
            FROM silver_worker
            WHERE manager_id IS NOT NULL
              AND manager_id NOT IN (SELECT worker_id FROM silver_worker)
        """,
    ),
    Check(
        name="sin_not_masked",
        description="Social Insurance Number must be masked as ***-***-NNN",
        violations_sql=r"""
            SELECT worker_id, sin_masked
            FROM silver_worker
            WHERE NOT regexp_matches(sin_masked, '^\*\*\*-\*\*\*-[0-9]{3}$')
        """,
    ),
    Check(
        name="gold_one_row_per_worker",
        description="The Gold layer must have exactly one row per worker",
        violations_sql="""
            SELECT worker_id, COUNT(*) AS rows_in_gold
            FROM gold_worker_current
            GROUP BY worker_id
            HAVING COUNT(*) > 1
        """,
    ),
]


def run_checks(con: duckdb.DuckDBPyConnection) -> list[dict]:
    """Run all checks and return the result of each one."""
    results = []
    for check in CHECKS:
        relation = con.sql(check.violations_sql)
        rows = relation.fetchall()
        results.append(
            {
                "check": check.name,
                "description": check.description,
                "status": "FAIL" if rows else "PASS",
                "violations": len(rows),
                "sample": "; ".join(str(row) for row in rows[:5]),
            }
        )
    return results
