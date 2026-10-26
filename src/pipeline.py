"""ساخت لایه‌های Bronze، Silver و Gold روی DuckDB."""
from pathlib import Path

import duckdb

from src.config import RAW_FILE


def build_layers(con: duckdb.DuckDBPyConnection, raw_file: str | Path = RAW_FILE) -> None:
    """داده خام را در سه لایه بار می‌کند."""
    raw_path = Path(raw_file).as_posix()

    # Bronze: داده خام، همه ستون‌ها به صورت متن
    con.execute(
        f"CREATE OR REPLACE TABLE bronze_workday AS "
        f"SELECT * FROM read_csv('{raw_path}', all_varchar = true)"
    )

    # Silver: نوع‌های درست و مقادیر خالی یکدست
    con.execute(
        """
        CREATE OR REPLACE TABLE silver_worker AS
        SELECT
            worker_id,
            worker_status,
            CAST(effective_date AS DATE)            AS effective_date,
            CAST(end_date AS DATE)                  AS end_date,
            NULLIF(job_code, '')                    AS job_code,
            NULLIF(manager_id, '')                  AS manager_id,
            location,
            CAST(NULLIF(hire_date, '') AS DATE)     AS hire_date,
            work_email,
            sin_masked
        FROM bronze_workday
        """
    )

    # Gold: آخرین وضعیت هر کارمند، یک ردیف برای هر کارمند
    con.execute(
        """
        CREATE OR REPLACE TABLE gold_worker_current AS
        SELECT *
        FROM silver_worker
        QUALIFY ROW_NUMBER() OVER (
            PARTITION BY worker_id
            ORDER BY effective_date DESC
        ) = 1
        """
    )
