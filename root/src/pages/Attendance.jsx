import { useEffect, useState } from "react";
import { fetchAttendance } from "../api/api";

export default function Attendance() {
  const [attendance, setAttendance] = useState([]);

  useEffect(() => {
    fetchAttendance().then(setAttendance);
  }, []);

  return (
    <div className="page-container">
      <h1>Attendance</h1>

      {attendance.map(a => {
        const percent = Math.round(
          (a.attended_classes / a.total_classes) * 100
        );
        return (
          <div key={a.id} className="card">
            Subject {a.subject_id} — {percent}%
          </div>
        );
      })}
    </div>
  );
}
