# Business Rules and Effective Dating

## Effective Date

- Every change in a worker's status or job creates a new record with a new `effective_date`.
- Each record covers the period from `effective_date` to `end_date`. If no later change exists, `end_date` is `9999-12-31`.
- A worker's periods must not overlap. On any given day, a worker has only one valid status.
- `end_date` must not be earlier than `effective_date`.

## Required Fields

- `worker_id`, `effective_date`, `hire_date`, and `job_code` must not be empty.
- `manager_id` can be empty (for example, for a top executive). If it has a value, it must point to an existing worker.

## Privacy

- The Social Insurance Number appears only in masked form (`***-***-NNN`) in any layer used for reporting.
- Work email is not kept in the Gold layer.

> These rules are examples. They must be reviewed and approved with the People Analytics and Data Governance teams.
