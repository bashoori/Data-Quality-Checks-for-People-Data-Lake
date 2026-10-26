# Data Quality Checks for People Data Lake

چارچوبی برای کنترل کیفیت داده‌های منابع انسانی که از Workday وارد Data Lake می‌شوند. پروژه بررسی می‌کند که داده در مسیر Bronze، Silver و Gold درست، کامل و قابل اعتماد باقی بماند، و نتیجه را به صورت فایل CSV ثبت می‌کند.

> این پروژه فقط با **داده ساختگی** کار می‌کند. داده واقعی کارکنان را وارد ریپو نکنید.

## چه کاری انجام می‌دهد

1. فایل خروجی Workday را می‌خواند و در سه لایه بار می‌کند:
   - **Bronze:** داده خام بدون تغییر
   - **Silver:** داده با نوع‌های درست (تاریخ و متن)
   - **Gold:** آخرین وضعیت هر کارمند (یک ردیف برای هر کارمند)
2. ۹ کنترل کیفیت را روی این لایه‌ها اجرا می‌کند.
3. نتیجهٔ هر کنترل (PASS یا FAIL) را با تعداد خطاها و نمونه‌ای از ردیف‌های خطادار در `qa/results/` ذخیره می‌کند.

## کنترل‌ها

| کنترل | چه چیزی را بررسی می‌کند |
|---|---|
| `reconciliation_row_count` | تعداد ردیف Bronze و Silver برابر باشد |
| `duplicate_worker_effective_date` | یک کارمند برای یک تاریخ مؤثر دو بار ثبت نشده باشد |
| `overlapping_effective_periods` | بازه‌های مؤثر یک کارمند روی هم نیفتند |
| `end_before_start` | تاریخ پایان قبل از تاریخ شروع نباشد |
| `missing_hire_date` | تاریخ استخدام خالی نباشد |
| `missing_job_code` | کد شغل خالی نباشد |
| `orphan_manager` | مدیر ثبت‌شده در فایل وجود داشته باشد |
| `sin_not_masked` | شمارهٔ بیمه اجتماعی ماسک شده باشد |
| `gold_one_row_per_worker` | در لایهٔ Gold هر کارمند فقط یک ردیف داشته باشد |

## ساختار پوشه‌ها

```
people-data-lake-qa/
├── data/
│   ├── raw/                  # داده ساختگی Workday
│   └── README.md             # خطاهای عمدی داخل داده
├── docs/
│   ├── source_to_target.md   # نگاشت فیلدهای Workday به لایه‌ها
│   ├── business_rules.md     # قوانین کسب‌وکار و effective dating
│   ├── qa_playbook.md        # روش تست و راهنمای triage
│   └── defect_log.md         # ثبت defectها
├── qa/
│   ├── checks.py             # تعریف کنترل‌های کیفیت
│   ├── run_all_checks.py     # نقطهٔ ورود اجرای کنترل‌ها
│   └── results/              # خروجی‌های CSV (در git نگه داشته نمی‌شوند)
├── src/
│   ├── config.py             # مسیرها و تنظیمات
│   └── pipeline.py           # ساخت لایه‌های Bronze، Silver و Gold
├── tests/
│   ├── conftest.py
│   └── test_checks.py        # تست‌های خود کنترل‌ها
├── .github/workflows/ci.yml  # اجرای تست‌ها و کنترل‌ها در هر push
├── requirements.txt
├── SETUP.md                  # راهنمای نصب
└── README.md
```

## راه‌اندازی

راهنمای کامل در `SETUP.md` است. خلاصه:

```bash
python -m venv .venv
source .venv/bin/activate        # در ویندوز: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## اجرا

اجرای همهٔ کنترل‌ها روی داده ساختگی:

```bash
python -m qa.run_all_checks
```

برای استفاده در pipeline واقعی، با پرچم `--strict` اجرا کنید تا در صورت وجود خطا کد خروج ۱ برگردد:

```bash
python -m qa.run_all_checks --strict
```

اجرای تست‌ها:

```bash
pytest tests/ -v
```

## نتیجهٔ نمونه

روی فایل ساختگی، ۷ کنترل FAIL و ۲ کنترل PASS می‌دهند. هر FAIL به یک خطای عمدی در `data/raw/workday_worker_extract.csv` مربوط است. جزئیات در `data/README.md` آمده است.

## مراحل بعدی

- داشبورد Power BI روی خروجی‌های CSV در `qa/results/`
- افزودن کنترل freshness و volume
- اتصال به Microsoft Fabric Lakehouse یا Databricks
- زمان‌بندی اجرا با Airflow
