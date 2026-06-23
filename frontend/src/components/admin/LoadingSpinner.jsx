function LoadingSpinner({ message = "Loading..." }) {
  return (
    <div className="loading-container" role="status" aria-live="polite">
      <div className="loading-bar-group" aria-hidden="true">
        <div className="loading-bar" />
        <div className="loading-bar" />
        <div className="loading-bar" />
        <div className="loading-bar" />
        <div className="loading-bar" />
      </div>
      <p className="loading-text">{message}</p>
    </div>
  );
}

export default LoadingSpinner;
