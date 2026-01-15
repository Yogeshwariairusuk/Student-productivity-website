import { Link } from "react-router-dom";
import "../styles/layout.css";

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <h2>🎓 Student Productivity</h2>
      <p className="tagline">Plan · Track · Succeed</p>

      <nav>
        <Link to="/">Dashboard</Link>
        <Link to="/subjects">Subjects</Link>
        <Link to="/tasks">Tasks</Link>
        <Link to="/assignments">Assignments</Link>
        <Link to="/attendance">Attendance</Link>
      </nav>
    </aside>
  );
}
