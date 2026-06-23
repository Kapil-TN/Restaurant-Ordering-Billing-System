function StatsCard({ label, value, prefix = "", icon, colorClass = "color-yellow" }) {
  const display =
    value !== undefined && value !== null
      ? `${prefix}${typeof value === "number" ? value.toLocaleString() : value}`
      : "—";

  return (
    <div className={`stat-card ${colorClass}`} role="region" aria-label={label}>
      <span className="stat-card-icon">{icon}</span>
      <p className="stat-card-label">{label}</p>
      <div className="stat-card-value">{display}</div>
    </div>
  );
}

export default StatsCard;
