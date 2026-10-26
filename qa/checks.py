"""کنترل‌های کیفیت داده برای لایه‌های People Data Lake.

هر کنترل یک کوئری دارد که ردیف‌های خطادار را برمی‌گرداند.
اگر کوئری هیچ ردیفی برنگرداند، کنترل PASS است.
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
        description="تعداد ردیف Bronze و Silver باید برابر باشد",
        violations_sql="""
            SELECT b.n AS bronze_rows, s.n AS silver_rows
            FROM (SELECT COUNT(*) AS n FROM bronze_workday) b,
                 (SELECT COUNT(*) AS n FROM silver_worker) s
            WHERE b.n <> s.n
        """,
    ),
    Check(
        name="duplicate_worker_effective_date",
        description="یک کارمند برای یک تاریخ مؤثر نباید بیش از یک رکورد داشته باشد",
        violations_sql="""
            SELECT worker_id, effective_date, COUNT(*) AS occurrences
            FROM silver_worker
            GROUP BY worker_id, effective_date
            HAVING COUNT(*) > 1
        """,
    ),
    Check(
        name="overlapping_effective_periods",
        description="بازه‌های مؤثر یک کارمند نباید روی هم بیفتند",
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
        description="تاریخ پایان نباید قبل از تاریخ شروع باشد",
        violations_sql="""
            SELECT worker_id, effective_date, end_date
            FROM silver_worker
            WHERE end_date < effective_date
        """,
    ),
    Check(
        name="missing_hire_date",
        description="تاریخ استخدام نباید خالی باشد",
        violations_sql="""
            SELECT worker_id, effective_date
            FROM silver_worker
            WHERE hire_date IS NULL
        """,
    ),
    Check(
        name="missing_job_code",
        description="کد شغل نباید خالی باشد",
        violations_sql="""
            SELECT worker_id, effective_date
            FROM silver_worker
            WHERE job_code IS NULL
        """,
    ),
    Check(
        name="orphan_manager",
        description="مدیر ثبت‌شده باید در فایل به عنوان کارمند وجود داشته باشد",
        violations_sql="""
            SELECT worker_id, manager_id
            FROM silver_worker
            WHERE manager_id IS NOT NULL
              AND manager_id NOT IN (SELECT worker_id FROM silver_worker)
        """,
    ),
    Check(
        name="sin_not_masked",
        description="شمارهٔ بیمه اجتماعی باید به شکل ***-***-NNN ماسک شده باشد",
        violations_sql=r"""
            SELECT worker_id, sin_masked
            FROM silver_worker
            WHERE NOT regexp_matches(sin_masked, '^\*\*\*-\*\*\*-[0-9]{3}$')
        """,
    ),
    Check(
        name="gold_one_row_per_worker",
        description="در لایهٔ Gold هر کارمند فقط یک ردیف داشته باشد",
        violations_sql="""
            SELECT worker_id, COUNT(*) AS rows_in_gold
            FROM gold_worker_current
            GROUP BY worker_id
            HAVING COUNT(*) > 1
        """,
    ),
]


def run_checks(con: duckdb.DuckDBPyConnection) -> list[dict]:
    """همه کنترل‌ها را اجرا و نتیجه هر کدام را برمی‌گرداند."""
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
