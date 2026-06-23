import { useState } from "react";
import { triggerExport, checkExportStatus } from "../../api/analyticsApi";

/**
 * NOT yet added to AdminDashboardPage by default — BJ-3 ownership
 * (customer-facing vs admin-facing export) is still pending a team
 * decision. The component is ready; import and render it once that's
 * confirmed. See README for details.
 */
function ExportButton({ customerId, customerEmail }) {
  const [status, setStatus] = useState("idle");

  async function handleExport() {
    setStatus("exporting");
    try {
      const { task_id } = await triggerExport(customerId, customerEmail);
      pollStatus(task_id);
    } catch (err) {
      setStatus("error");
    }
  }

  function pollStatus(taskId) {
    const interval = setInterval(async () => {
      try {
        const data = await checkExportStatus(taskId);
        if (data.status === "SUCCESS") {
          clearInterval(interval);
          setStatus("done");
        } else if (data.status === "FAILURE") {
          clearInterval(interval);
          setStatus("error");
        }
      } catch {
        clearInterval(interval);
        setStatus("error");
      }
    }, 2000);
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
      <button
        className="export-btn"
        id="export-order-history-btn"
        onClick={handleExport}
        disabled={status === "exporting"}
      >
        {status === "exporting" ? "⏳ Exporting…" : "⬇️ Export CSV"}
      </button>
      {status === "done" && (
        <p style={{ fontSize: '0.78rem', color: '#34d399', margin: 0 }}>
          ✓ Done! Check your email.
        </p>
      )}
      {status === "error" && (
        <p style={{ fontSize: '0.78rem', color: '#fb7185', margin: 0 }}>
          ✗ Something went wrong. Try again.
        </p>
      )}
    </div>
  );
}

export default ExportButton;
