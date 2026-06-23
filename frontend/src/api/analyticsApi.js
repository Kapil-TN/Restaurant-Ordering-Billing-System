// IMPORTANT: using 127.0.0.1 instead of "localhost" deliberately.
// On some Windows machines, "localhost" resolves to an IPv6 address (::1)
// that Flask's dev server isn't listening on, causing silent connection
// failures. 127.0.0.1 is unambiguous and avoids that entirely.
const API_BASE_URL = "http://127.0.0.1:5000";

export async function getDashboardSummary() {
  const response = await fetch(`${API_BASE_URL}/admin/dashboard`);
  if (!response.ok) throw new Error("Failed to load dashboard data");
  return response.json();
}

export async function getAnalytics() {
  const response = await fetch(`${API_BASE_URL}/admin/analytics`);
  if (!response.ok) throw new Error("Failed to load analytics data");
  return response.json();
}

export async function triggerExport(customerId, customerEmail) {
  const response = await fetch(`${API_BASE_URL}/admin/export`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ customer_id: customerId, customer_email: customerEmail }),
  });
  if (!response.ok) throw new Error("Failed to start export");
  return response.json();
}

export async function checkExportStatus(taskId) {
  const response = await fetch(`${API_BASE_URL}/admin/export/status/${taskId}`);
  if (!response.ok) throw new Error("Failed to check export status");
  return response.json();
}
