import { useEffect, useState } from "react";
import { fetchSubjects, createSubject } from "../api/api";
import "../styles/common.css";

export default function Subjects() {
  const [subjects, setSubjects] = useState([]);
  const [name, setName] = useState("");

  useEffect(() => {
    loadSubjects();
  }, []);

  const loadSubjects = async () => {
    const data = await fetchSubjects();
    setSubjects(data);
  };

  const addSubject = async () => {
    if (!name.trim()) return;
    await createSubject({ name });
    setName("");
    loadSubjects();
  };

  return (
    <div className="page-container">
      <h1>Subjects</h1>

      {/* ADD FORM */}
      <div className="form-row">
        <input
          value={name}
          onChange={e => setName(e.target.value)}
          placeholder="New subject"
        />
        <button onClick={addSubject}>Add Subject</button>
      </div>

      {/* LIST */}
      {subjects.map(s => (
        <div key={s.id} className="card list-item">
          {s.name}
        </div>
      ))}
    </div>
  );
}
