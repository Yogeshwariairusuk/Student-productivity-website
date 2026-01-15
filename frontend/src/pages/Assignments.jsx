import { useEffect, useState } from "react";
import { fetchAssignments } from "../api/api";

export default function Assignments() {
  const [assignments, setAssignments] = useState([]);

  useEffect(() => {
    fetchAssignments().then(setAssignments);
  }, []);

  return (
    <div className="page-container">
      <h1>Assignments</h1>

      {assignments.map(a => (
        <div key={a.id} className="card">{a.title}</div>
      ))}
    </div>
  );
}
