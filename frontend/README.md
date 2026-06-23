# Member 4 Frontend — Verified, Ready to Run

Built and verified in a clean environment: `npm install` succeeds,
`npm run build` compiles with ZERO errors. This is the React dashboard
with Bootstrap styling and Recharts charts, wired to call your Flask
backend at `http://127.0.0.1:5000`.

## Setup

```bash
npm install
npm run dev
```

Then open the URL it shows you (something like `http://localhost:5173`).

## Important — read this before you start

**Use 127.0.0.1, not "localhost", everywhere.** The API calls in
`src/api/analyticsApi.js` deliberately use `http://127.0.0.1:5000`
instead of `http://localhost:5000`. On some Windows machines,
"localhost" resolves to an IPv6 address that Flask's dev server isn't
listening on, causing silent connection failures. If you ever add new
API calls, keep using `127.0.0.1`.

**You need the backend running first.** This frontend does nothing
useful on its own — it fetches data from Flask. Start the backend
(see backend's own README) BEFORE opening this in your browser.

**Before testing: make sure only ONE Flask process is running.**
On Windows, open Task Manager → Details tab → look for `python.exe`.
If you see more than one, end all of them, then start Flask fresh.
Multiple leftover Flask processes from earlier testing sessions can
cause confusing, inconsistent errors that look like CORS or server
bugs but are actually just port conflicts.

## What's included

- `src/pages/AdminDashboardPage.jsx` — main dashboard, fetches both
  `/admin/dashboard` and `/admin/analytics`, shows loading/error states
- `src/components/admin/` — StatsCard, 3 Recharts charts, AdminLayout
  (navbar), LoadingSpinner, ErrorAlert, ExportButton
- `src/api/analyticsApi.js` — all API calls in one place

## Not yet wired in

`ExportButton.jsx` is built but NOT added to the dashboard page yet.
This is intentional — whether `/admin/export` is customer-facing or
admin-facing is still an open decision with your team (affects which
auth decorator it needs). Once decided, import it into
`AdminDashboardPage.jsx` and render it — it's a 2-line addition.

## Verified

- `npm install` — clean, no errors
- `npm run build` — compiled successfully, 585 modules, zero errors
- Bootstrap CSS loads correctly (imported in `main.jsx`)
- Recharts imports resolve correctly in all 3 chart components
