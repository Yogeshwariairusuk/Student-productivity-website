export default function StatCard({ title, value, color }) {
  return (
    <div className="stat-card" style={{ borderLeftColor: color }}>
      <p className="stat-title">{title}</p>
      <h2 className="stat-value">{value}</h2>
    </div>
  );
}
