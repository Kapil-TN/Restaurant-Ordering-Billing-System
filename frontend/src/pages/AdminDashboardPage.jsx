import { useEffect, useState, useCallback } from "react";
import { getDashboardSummary, getAnalytics } from "../api/analyticsApi";
import StatsCard from "../components/admin/StatsCard";
import BestSellersChart from "../components/admin/BestSellersChart";
import OrderTypePieChart from "../components/admin/OrderTypePieChart";
import RevenueTrendChart from "../components/admin/RevenueTrendChart";
import LoadingSpinner from "../components/admin/LoadingSpinner";
import ErrorAlert from "../components/admin/ErrorAlert";
import AdminLayout from "../components/admin/AdminLayout";

function AdminDashboardPage() {
  const [dashboard, setDashboard] = useState(null);
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadData = useCallback(() => {
    setLoading(true);
    setError(null);
    Promise.all([getDashboardSummary(), getAnalytics()])
      .then(([dashboardData, analyticsData]) => {
        setDashboard(dashboardData);
        setAnalytics(analyticsData);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const pct = analytics?.revenue?.revenue_change_percentage ?? 0;
  const isPositive = pct >= 0;

  return (
    <AdminLayout>
      {loading && <LoadingSpinner message="Fetching dashboard data…" />}
      {error && <ErrorAlert message={error} onRetry={loadData} />}

      {!loading && !error && dashboard && analytics && (
        <>
          {/* ── Page Header ──────────────────────────── */}
          <div className="page-header">
            <h1 className="page-title">Dashboard</h1>
            <p className="page-subtitle">Real-time overview of restaurant performance</p>
          </div>

          {/* ── Stat Cards ───────────────────────────── */}
          <div className="stats-grid">
            <StatsCard
              label="Total Revenue"
              value={analytics.revenue.total_revenue}
              prefix="₹"
              icon="💰"
              colorClass="color-purple"
            />
            <StatsCard
              label="Total Orders"
              value={dashboard.total_orders}
              icon="🧾"
              colorClass="color-cyan"
            />
            <StatsCard
              label="Total Customers"
              value={dashboard.total_customers}
              icon="👥"
              colorClass="color-green"
            />
            <StatsCard
              label="Pending Orders"
              value={dashboard.pending_orders}
              icon="⏳"
              colorClass="color-rose"
            />
          </div>

          {/* ── Revenue Banner ───────────────────────── */}
          <div className={`revenue-banner ${isPositive ? "positive" : "negative"}`}>
            <span className="revenue-banner-icon">{isPositive ? "📈" : "📉"}</span>
            <div className="revenue-banner-text">
              Today's revenue:&nbsp;
              <strong>₹{analytics.revenue.today_revenue.toLocaleString()}</strong>
              &nbsp;vs yesterday's&nbsp;
              <strong>₹{analytics.revenue.yesterday_revenue.toLocaleString()}</strong>
            </div>
            <span className="revenue-change-badge">
              {isPositive ? "▲" : "▼"} {Math.abs(pct)}%
            </span>
          </div>

          {/* ── Charts ───────────────────────────────── */}
          <div className="charts-grid">
            <BestSellersChart data={analytics.best_sellers} />
            <OrderTypePieChart data={analytics.order_type_distribution} />
            <RevenueTrendChart data={analytics.revenue_trend} />
          </div>
        </>
      )}
    </AdminLayout>
  );
}

export default AdminDashboardPage;
