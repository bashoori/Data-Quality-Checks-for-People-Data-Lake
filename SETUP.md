# Setup Guide

This guide prepares the local environment for the Data Quality Checks for People Data Lake project. Estimated time: about 15 minutes.

## Prerequisites

- **Python 3.10 or higher**
  - Check your version: `python --version` or `python3 --version`
  - Download: https://www.python.org/downloads/
- **Git** (optional, for working with GitHub)
- **Power BI Desktop** (Windows only, for building the QA dashboard later)
  - Download: Microsoft Store or https://powerbi.microsoft.com/desktop/

## 1. Create a Virtual Environment

A virtual environment keeps this project's dependencies separate from your other projects.

**Windows (PowerShell):**
```powershell
cd data-quality-checks-for-people-data-lake
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS and Linux:**
```bash
cd data-quality-checks-for-people-data-lake
python3 -m venv .venv
source .venv/bin/activate
```

When activated, the prompt starts with `(.venv)`.

> If PowerShell blocks the activation script, run this once:
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

## 2. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Verify the Installation

```bash
python -c "import pandas, duckdb, pytest, openpyxl; print('pandas', pandas.__version__); print('duckdb', duckdb.__version__); print('pytest', pytest.__version__); print('openpyxl', openpyxl.__version__)"
```

If all four versions are printed, the installation is complete.

## 4. Test DuckDB

```bash
python -c "import duckdb; print(duckdb.sql('SELECT 1 AS ok').fetchall())"
```

The output should be `[(1,)]`.

## 5. Run the Tests

```bash
pytest tests/ -v
```

## Troubleshooting

| Problem | Solution |
|---|---|
| `python` not found | Use `python3`, or reinstall Python and enable "Add to PATH". |
| `pip` is outdated | `python -m pip install --upgrade pip` |
| `duckdb` fails to install | Check your Python version (must be 3.10 or higher). |
| `Activate.ps1` will not run | Run the `Set-ExecutionPolicy` command in step 1. |

## Note on Data

This project works only with **synthetic data**. Never place real employee data in the repository, even for testing.
