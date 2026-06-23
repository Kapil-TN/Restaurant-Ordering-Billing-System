# Member 4 Backend — Verified Package (with CORS fix)

This is the exact code built and tested in this conversation. Every
file has been run and confirmed working — including a genuine
end-to-end CORS test via real `curl` requests with an `Origin` header,
not just code review.

## ⚠️ Before you use this

- `app/__init__.py` and `app/admin/placeholder_models.py` are TEMPORARY
  stand-ins for Member 1's auth/Flask setup and Member 3's real models.
  Delete these two files once your teammates commit their real
  versions, and update the import lines noted in the comments inside
  `analytics.py` and `tasks.py`.
- `.env` is NOT included (never commit it). Create your own with
  `MAIL_USERNAME` and `MAIL_PASSWORD` for real email sending — without
  it, `send_email()` falls back to printing to console, which is fine
  for development.

## Setup

```bash
pip install -r requirements.txt
python seed_test_data.py      # creates restaurant.db with realistic fake data
python -m pytest tests/ -v     # runs 10 automated tests, all should PASS
python run.py                  # starts Flask on 127.0.0.1:5000
```

**Before running `python run.py`: make sure no other Flask process is
already running.** On Windows, check Task Manager -> Details tab ->
look for `python.exe`. End any leftover ones first. Running two Flask
servers at once on the same port causes confusing, inconsistent
errors (sometimes 500, sometimes connection refused) that look like
bugs but are actually just port conflicts from an old process never
being stopped.

For Celery (separate terminals, requires a running Redis/Memurai server):
```bash
celery -A app.celery_worker.celery_app worker --loglevel=info --pool=solo
celery -A app.celery_worker.celery_app beat --loglevel=info
```
(`--pool=solo` is required on Windows.)

## CORS - now fixed and verified

`flask-cors` is installed and `CORS(app)` is active in `app/__init__.py`.
This was tested with a REAL `curl` request including an `Origin` header
(simulating exactly what a browser sends) and confirmed the response
includes `Access-Control-Allow-Origin`. If your frontend still shows a
CORS-looking error, it is almost certainly NOT actually a CORS problem -
check for: (a) more than one Flask process running, (b) the frontend
calling the wrong port, or (c) Flask not actually being restarted after
a code change.

## What was verified (in a clean sandbox, June 2026)

- `seed_test_data.py` runs without errors
- All 7 `analytics.py` functions return correct values against seeded data
- `GET /admin/dashboard` and `GET /admin/analytics` both return 200 with
  correctly-shaped JSON
- All 10 pytest assertions pass (fixed-value tests, not random data)
- `generate_csv_export` produces a real, correctly-joined CSV file
- `send_monthly_report` produces correct revenue/top-items/busiest-day
- `send_reengagement_emails` proven correct (not just silent) - a
  deliberately inactive test customer was added and correctly flagged
- Full live stack tested together: real Redis + real Flask + real
  Celery worker + real Celery beat, all connected and working
- `cache.py` fails open gracefully if Redis isn't running (doesn't crash)
- CORS verified with a real HTTP request including an Origin header -
  confirmed Access-Control-Allow-Origin is present on real responses

## Still open (not fixable without your team)

- Swap `placeholder_models.py` for Member 3's real Order/OrderItem/Bill
  and Member 1's real User model
- Add Member 1's real @admin_required JWT decorator to the routes
- Confirm the revenue business rule (which date field, which bill
  status counts) - see ONLY_COUNT_PAID_BILLS in analytics.py
- Confirm BJ-3 ownership (customer vs admin export) - affects the auth
  decorator on POST /admin/export
- Replace the hardcoded admin_email in send_monthly_report with a
  real query once Member 1's User model has a role field
