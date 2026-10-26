# نگاشت Source به Target

| فیلد منبع (Workday) | Bronze | Silver | Gold | قانون یا تبدیل |
|---|---|---|---|---|
| worker_id | `worker_id` | `worker_id` | `worker_id` | کلید کارمند، الزامی |
| worker_status | `worker_status` | `worker_status` | `worker_status` | بدون تغییر |
| effective_date | `effective_date` (متن) | `effective_date` (DATE) | `effective_date` | تبدیل به DATE |
| end_date | `end_date` (متن) | `end_date` (DATE) | `end_date` | تبدیل به DATE، ۹۹۹۹-۱۲-۳۱ یعنی بدون پایان |
| job_code | `job_code` (متن) | `job_code` | `job_code` | رشتهٔ خالی به NULL |
| manager_id | `manager_id` (متن) | `manager_id` | `manager_id` | رشتهٔ خالی به NULL |
| location | `location` | `location` | `location` | بدون تغییر |
| hire_date | `hire_date` (متن) | `hire_date` (DATE) | `hire_date` | رشتهٔ خالی به NULL |
| work_email | `work_email` | `work_email` | حذف شود | در لایهٔ Gold نباید باشد |
| sin_masked | `sin_masked` | `sin_masked` | `sin_masked` | باید به شکل ***-***-NNN باشد |

## قوانین عمومی

- Bronze هیچ تغییری ندارد. هر تبدیل فقط در Silver انجام می‌شود.
- Gold فقط آخرین رکورد هر کارمند بر اساس `effective_date` را نگه می‌دارد.
- هر ستونی که به Gold می‌رسد باید در گزارش‌ها هم قابل استفاده باشد. ستون‌های حساس باید ماسک شده باشند.
