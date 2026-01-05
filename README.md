# Reconciliation Component (Django)

This repository contains a reusable reconciliation component that can be plugged into Django projects. It includes:

- A minimal Django project configuration for local experimentation.
- A `reconciliation` app with models to store runs, rules, records, and match results.
- A pure-Python reconciliation engine that can be reused independently of Django views.
- A demonstration view/URL that shows how to wire the engine into HTTP.

## Key concepts
- **FieldRule**: defines how to compare a field between source and target (metric, weight, tolerance).
- **ReconciliationConfig**: aggregates field rules with thresholds for confidence and auto-approval.
- **Reconciler**: applies rules to two datasets and returns match results.
- **MatchResult**: structured outcome with score, field-by-field details, and decision.

## Quick start
1. Install dependencies (Django 5+ recommended):
   ```bash
   pip install "django>=5.0"
   ```
2. Run migrations:
   ```bash
   python manage.py migrate
   ```
3. Start the server and post JSON to `/reconciliation/matches/` to see matches:
   ```bash
   python manage.py runserver
   ```

## Parameters considered
- **field rules**: source key, target key, metric (`string` or `numeric`), weight, tolerance.
- **thresholds**: `min_confidence` and `auto_approve_threshold` to decide whether a match is auto-approved, needs review, or rejected.

## Scenarios covered
- Fuzzy name matching using sequence similarity for strings.
- Numeric comparisons with configurable tolerance (useful for currency/quantity fields).
- Weighted scoring across multiple fields to control the influence of each attribute.
- Automatic approval for high confidence matches; optional manual review for borderline results; rejection of low scores.
- Storage models for reconciliation runs and match candidates if you need persistence.

## Running tests
The pure-Python reconciler has a sample test that can be run with `pytest`:

```bash
pytest tests/test_reconciliation.py
```
