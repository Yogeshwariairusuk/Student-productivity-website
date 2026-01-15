const BASE = "http://127.0.0.1:8000";

export const fetchDashboard = async () =>
  fetch(`${BASE}/dashboard`).then(res => res.json());

export const fetchSubjects = async () =>
  fetch(`${BASE}/subjects`).then(res => res.json());

export const createSubject = async (data) =>
  fetch(`${BASE}/subjects`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });

export const fetchTasks = async () =>
  fetch(`${BASE}/tasks`).then(res => res.json());

export const createTask = async (data) =>
  fetch(`${BASE}/tasks`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });

export const fetchAssignments = async () =>
  fetch(`${BASE}/assignments`).then(res => res.json());

export const fetchAttendance = async () =>
  fetch(`${BASE}/attendance`).then(res => res.json());
