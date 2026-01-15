from pydantic import BaseModel

class SubjectCreate(BaseModel):
    name: str

class SubjectResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

from datetime import date

class TaskCreate(BaseModel):
    title: str
    subject_id: int
    priority: str
    status: str
    due_date: date

class TaskResponse(BaseModel):
    id: int
    title: str
    subject_id: int
    priority: str
    status: str
    due_date: date

    class Config:
        from_attributes = True

class AssignmentCreate(BaseModel):
    title: str
    subject_id: int
    due_date: date
    status: str

class AssignmentResponse(BaseModel):
    id: int
    title: str
    subject_id: int
    due_date: date
    status: str

    class Config:
        from_attributes = True

class AttendanceCreate(BaseModel):
    subject_id: int
    total_classes: int
    attended_classes: int

class AttendanceResponse(BaseModel):
    id: int
    subject_id: int
    total_classes: int
    attended_classes: int
    attendance_percentage: float

    class Config:
        from_attributes = True

class DashboardResponse(BaseModel):
    total_subjects: int
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    total_assignments: int
    pending_assignments: int
    attendance_alerts: list[int]  # subject_ids below 75%
