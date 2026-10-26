# راهنمای نصب و راه‌اندازی

این راهنما محیط اولیهٔ پروژه Data Quality Checks for People Data Lake را آماده می‌کند. زمان لازم: حدود ۱۵ دقیقه.

## پیش‌نیازها

- **Python 3.10 یا بالاتر**
  - بررسی نسخه: `python --version` یا `python3 --version`
  - دانلود: https://www.python.org/downloads/
- **Git** (اختیاری، برای کار با GitHub)
- **Power BI Desktop** (فقط ویندوز، برای ساخت داشبورد QA)
  - دانلود: از Microsoft Store یا https://powerbi.microsoft.com/desktop/

## ۱. ساخت محیط مجازی

محیط مجازی باعث می‌شود وابستگی‌های این پروژه با بقیهٔ پروژه‌های شما تداخل نداشته باشند.

**Windows (PowerShell):**
```powershell
cd people-data-lake-qa
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS و Linux:**
```bash
cd people-data-lake-qa
python3 -m venv .venv
source .venv/bin/activate
```

اگر فعال‌سازی انجام شده باشد، ابتدای خط فرمان `(.venv)` نمایش داده می‌شود.

> اگر در PowerShell خطای اجازه دیدید، این دستور را یک‌بار اجرا کنید:
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

## ۲. نصب وابستگی‌ها

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## ۳. بررسی نصب

یک فایل کوچک برای تست بسازید یا این دستور را در ترمینال اجرا کنید:

```bash
python -c "import pandas, duckdb, pytest, openpyxl; print('pandas', pandas.__version__); print('duckdb', duckdb.__version__); print('pytest', pytest.__version__); print('openpyxl', openpyxl.__version__)"
```

اگر چهار نسخه نمایش داده شدند، نصب کامل است.

## ۴. تست اولیهٔ SQL روی DuckDB

این تست نشان می‌دهد که موتور SQL محلی کار می‌کند:

```bash
python -c "import duckdb; print(duckdb.sql('SELECT 1 AS ok').fetchall())"
```

خروجی باید `[(1,)]` باشد.

## ۵. اجرای تست‌ها

بعد از اینکه تست‌های پروژه نوشته شدند، با این دستور اجرا کنید:

```bash
pytest tests/ -v
```

## عیب‌یابی سریع

| مشکل | راه‌حل |
|---|---|
| `python` پیدا نمی‌شود | از `python3` استفاده کنید یا Python را دوباره نصب کنید و گزینهٔ Add to PATH را فعال کنید. |
| `pip` قدیمی است | `python -m pip install --upgrade pip` |
| خطا در نصب `duckdb` | نسخهٔ Python را بررسی کنید (باید ۳.۱۰ یا بالاتر باشد). |
| `Activate.ps1` اجرا نمی‌شود | دستور `Set-ExecutionPolicy` را در بخش ۱ اجرا کنید. |

## یادداشت دربارهٔ داده

این پروژه فقط با **داده ساختگی** کار می‌کند. هیچ داده واقعی کارکنان را در ریپو قرار ندهید، حتی برای تست.
