# QA Playbook

This document describes the testing process and the QA team's workflow for the People Data Lake.

## 1. Before Each Release

1. Define the scope of the change: a new source, a change in transformation logic, or a new dashboard.
2. Update the source-to-target mapping (`docs/source_to_target.md`).
3. Record any new business rules in `docs/business_rules.md`.
4. Add or update the related checks in `qa/checks.py`.

## 2. Running the Tests

```bash
python -m qa.run_all_checks --strict
pytest tests/ -v
```

- Each FAIL must either be fixed or recorded in `defect_log.md` with an explanation.
- The CSV output in `qa/results/` must be kept as release evidence.

## 3. Defect Triage

| Severity | Definition | Response time |
|---|---|---|
| Critical | A management report is wrong, or sensitive data is not masked | Same day |
| High | A reconciliation or effective dating check fails | 2 business days |
| Medium | A non-critical field is incomplete | 5 business days |
| Low | A documentation or naming issue | Next version |

## 4. Status Report

Each release is closed with:
- Number of PASS and FAIL results
- List of open defects
- A go or no-go recommendation, with the reason

## 5. Adding a New Check

1. Add the check to `qa/checks.py` with a clear name and a short description.
2. Add sample data that contains the defect to `data/raw/`, and document it in `data/README.md`.
3. Write a test in `tests/test_checks.py`.
4. Add the check to the checks table in `README.md`.
