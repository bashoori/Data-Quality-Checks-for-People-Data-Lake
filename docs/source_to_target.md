# Source-to-Target Mapping

| Source field (Workday) | Bronze | Silver | Gold | Rule or transformation |
|---|---|---|---|---|
| worker_id | `worker_id` | `worker_id` | `worker_id` | Worker key, required |
| worker_status | `worker_status` | `worker_status` | `worker_status` | No change |
| effective_date | `effective_date` (text) | `effective_date` (DATE) | `effective_date` | Cast to DATE |
| end_date | `end_date` (text) | `end_date` (DATE) | `end_date` | Cast to DATE. 9999-12-31 means no end date |
| job_code | `job_code` (text) | `job_code` | `job_code` | Empty string becomes NULL |
| manager_id | `manager_id` (text) | `manager_id` | `manager_id` | Empty string becomes NULL |
| location | `location` | `location` | `location` | No change |
| hire_date | `hire_date` (text) | `hire_date` (DATE) | `hire_date` | Empty string becomes NULL |
| work_email | `work_email` | `work_email` | Removed | Must not appear in the Gold layer |
| sin_masked | `sin_masked` | `sin_masked` | `sin_masked` | Must be masked as ***-***-NNN |

## General Rules

- Bronze is never changed. All transformations happen in Silver.
- Gold keeps only the latest record per worker, based on `effective_date`.
- Every column that reaches Gold must be safe to use in reports. Sensitive columns must be masked.
