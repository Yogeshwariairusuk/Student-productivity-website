import { useEffect, useState } from "react";
import { fetchDashboard } from "../api/api";
import StatCard from "../components/StatCard";
import "../styles/dashboard.css";

export default function Dashboard() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetchDashboard().then(setData);
  }, []);

  if (!data) return <p className="loading">Loading dashboard...</p>;

  return (
    <div className="dashboard-container">
      <h1>Dashboard Overview</h1>

      {/* TOP ROW */}
      <div className="stats-grid primary">
        <StatCard title="Subjects" value={data.total_subjects} />
        <StatCard title="Total Tasks" value={data.total_tasks} />
        <StatCard title="Completed Tasks" value={data.completed_tasks} />
        <StatCard title="Assignments" value={data.total_assignments} />
      </div>

      {/* BOTTOM ROW */}
      <div className="stats-grid secondary">
        <StatCard title="Pending Tasks" value={data.pending_tasks} />
        <StatCard title="Pending Assignments" value={data.pending_assignments} />
        <StatCard
          title="Attendance Alerts"
          value={data.attendance_alerts.length}
        />
      </div>
    </div>
  );
}
