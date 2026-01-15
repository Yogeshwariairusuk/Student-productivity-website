import { useEffect, useState } from "react";
import { fetchTasks, createTask } from "../api/api";

export default function Tasks() {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState("");

  useEffect(() => {
    fetchTasks().then(setTasks);
  }, []);

  const addTask = async () => {
    if (!title) return;
    await createTask({ title, status: "pending" });
    setTitle("");
    fetchTasks().then(setTasks);
  };

  return (
    <div className="page-container">
      <h1>Tasks</h1>

      <input
        placeholder="New task"
        value={title}
        onChange={e => setTitle(e.target.value)}
      />
      <button onClick={addTask}>Add Task</button>

      {tasks.map(t => (
        <div key={t.id} className="card">
          {t.title} — {t.status}
        </div>
      ))}
    </div>
  );
}
