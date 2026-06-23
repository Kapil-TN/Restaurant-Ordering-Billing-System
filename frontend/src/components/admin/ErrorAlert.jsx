function ErrorAlert({ message, onRetry }) {
  return (
    <div className="error-container" role="alert">
      <div className="error-box">
        <span className="error-icon">✖</span>
        <div className="error-title">Failed to load dashboard</div>
        <p className="error-message">{message}</p>
        {onRetry && (
          <button
            className="error-retry-btn"
            onClick={onRetry}
            id="retry-dashboard-btn"
          >
            ↻ Retry
          </button>
        )}
      </div>
    </div>
  );
}

export default ErrorAlert;
