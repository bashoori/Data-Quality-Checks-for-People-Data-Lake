# Synthetic Workday Data

The file `raw/workday_worker_extract.csv` is synthetic data with intentional defects. The QA checks should detect these defects.

## Intentional Defects

| Worker | Defect | Check that should catch it |
|---|---|---|
| W1002 | Two records with consecutive periods (valid, a good example) | None (no defect) |
| W1003 | `manager_id` is `W9999`, which does not exist | `orphan_manager` |
| W1003 | `hire_date` is empty | `missing_hire_date` |
| W1005 | Effective periods overlap | `overlapping_effective_periods` |
| W1006 | `end_date` is before `effective_date` | `end_before_start` |
| W1007 | `job_code` is empty in one of the two records | `missing_job_code` |
| W1007 | Two records with the same effective date | `duplicate_worker_effective_date` |
| W1004 | `sin_masked` is not masked and shows the full number | `sin_not_masked` |

## Notes

- W1002 is intentionally valid, to show that the checks do not produce false positives.
- The Social Insurance Number values in this file are fictional and do not belong to any real person.
