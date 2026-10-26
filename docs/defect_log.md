# Defect Log

| ID | Check | Worker | Description | Severity | Status |
|---|---|---|---|---|---|
| DEF-001 | duplicate_worker_effective_date | W1007 | Two records with the same effective date | High | Open (intentional sample defect) |
| DEF-002 | overlapping_effective_periods | W1005 | Effective periods overlap | High | Open (intentional sample defect) |
| DEF-003 | end_before_start | W1006 | End date is before the start date | High | Open (intentional sample defect) |
| DEF-004 | missing_hire_date | W1003 | Hire date is empty | Medium | Open (intentional sample defect) |
| DEF-005 | missing_job_code | W1007 | Job code is empty in one record | Medium | Open (intentional sample defect) |
| DEF-006 | orphan_manager | W1003 | Manager W9999 does not exist in the file | High | Open (intentional sample defect) |
| DEF-007 | sin_not_masked | W1004 | Social Insurance Number is not masked | Critical | Open (intentional sample defect) |

> For real data, record each FAIL as a new row with an ID, an owner, and a date.
