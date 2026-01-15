from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal
import models
import schemas
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(title="Student Productivity API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# This line CREATES tables in PostgreSQL
Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"status": "Database connected & tables created"}

# -------------------------
# SUBJECT APIs
# -------------------------

@app.post("/subjects", response_model=schemas.SubjectResponse)
def create_subject(subject: schemas.SubjectCreate, db: Session = Depends(get_db)):
    new_subject = models.Subject(name=subject.name)
    db.add(new_subject)
    db.commit()
    db.refresh(new_subject)
    return new_subject

@app.get("/subjects", response_model=list[schemas.SubjectResponse])
def get_subjects(db: Session = Depends(get_db)):
    return db.query(models.Subject).all()

@app.put("/subjects/{subject_id}", response_model=schemas.SubjectResponse)
def update_subject(
    subject_id: int,
    subject: schemas.SubjectCreate,
    db: Session = Depends(get_db)
):
    db_subject = db.query(models.Subject).filter(models.Subject.id == subject_id).first()

    if not db_subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    db_subject.name = subject.name
    db.commit()
    db.refresh(db_subject)
    return db_subject


@app.delete("/subjects/{subject_id}")
def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    db_subject = db.query(models.Subject).filter(models.Subject.id == subject_id).first()

    if not db_subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    db.delete(db_subject)
    db.commit()
    return {"message": "Subject deleted successfully"}

# -------------------------
# TASK APIs
# -------------------------

@app.post("/tasks", response_model=schemas.TaskResponse)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    new_task = models.Task(
        title=task.title,
        subject_id=task.subject_id,
        priority=task.priority,
        status=task.status,
        due_date=task.due_date
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@app.get("/tasks", response_model=list[schemas.TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(models.Task).all()


@app.get("/subjects/{subject_id}/tasks", response_model=list[schemas.TaskResponse])
def get_tasks_by_subject(subject_id: int, db: Session = Depends(get_db)):
    return db.query(models.Task).filter(models.Task.subject_id == subject_id).all()


@app.put("/tasks/{task_id}", response_model=schemas.TaskResponse)
def update_task(task_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    db_task.title = task.title
    db_task.subject_id = task.subject_id
    db_task.priority = task.priority
    db_task.status = task.status
    db_task.due_date = task.due_date

    db.commit()
    db.refresh(db_task)
    return db_task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(db_task)
    db.commit()
    return {"message": "Task deleted successfully"}


# -------------------------
# ASSIGNMENT APIs
# -------------------------

@app.post("/assignments", response_model=schemas.AssignmentResponse)
def create_assignment(
    assignment: schemas.AssignmentCreate,
    db: Session = Depends(get_db)
):
    new_assignment = models.Assignment(
        title=assignment.title,
        subject_id=assignment.subject_id,
        due_date=assignment.due_date,
        status=assignment.status
    )
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)
    return new_assignment


@app.get("/assignments", response_model=list[schemas.AssignmentResponse])
def get_assignments(db: Session = Depends(get_db)):
    return db.query(models.Assignment).all()


@app.get("/subjects/{subject_id}/assignments", response_model=list[schemas.AssignmentResponse])
def get_assignments_by_subject(subject_id: int, db: Session = Depends(get_db)):
    return db.query(models.Assignment).filter(
        models.Assignment.subject_id == subject_id
    ).all()


@app.put("/assignments/{assignment_id}", response_model=schemas.AssignmentResponse)
def update_assignment(
    assignment_id: int,
    assignment: schemas.AssignmentCreate,
    db: Session = Depends(get_db)
):
    db_assignment = db.query(models.Assignment).filter(
        models.Assignment.id == assignment_id
    ).first()

    if not db_assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    db_assignment.title = assignment.title
    db_assignment.subject_id = assignment.subject_id
    db_assignment.due_date = assignment.due_date
    db_assignment.status = assignment.status

    db.commit()
    db.refresh(db_assignment)
    return db_assignment


@app.delete("/assignments/{assignment_id}")
def delete_assignment(assignment_id: int, db: Session = Depends(get_db)):
    db_assignment = db.query(models.Assignment).filter(
        models.Assignment.id == assignment_id
    ).first()

    if not db_assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    db.delete(db_assignment)
    db.commit()
    return {"message": "Assignment deleted successfully"}

# -------------------------
# ATTENDANCE APIs
# -------------------------

@app.post("/attendance", response_model=schemas.AttendanceResponse)
def create_attendance(
    attendance: schemas.AttendanceCreate,
    db: Session = Depends(get_db)
):
    record = models.Attendance(
        subject_id=attendance.subject_id,
        total_classes=attendance.total_classes,
        attended_classes=attendance.attended_classes
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    percentage = (
        record.attended_classes / record.total_classes * 100
        if record.total_classes > 0 else 0
    )

    return {
        "id": record.id,
        "subject_id": record.subject_id,
        "total_classes": record.total_classes,
        "attended_classes": record.attended_classes,
        "attendance_percentage": round(percentage, 2)
    }


@app.get("/attendance", response_model=list[schemas.AttendanceResponse])
def get_attendance(db: Session = Depends(get_db)):
    records = db.query(models.Attendance).all()
    result = []

    for r in records:
        percentage = (
            r.attended_classes / r.total_classes * 100
            if r.total_classes > 0 else 0
        )
        result.append({
            "id": r.id,
            "subject_id": r.subject_id,
            "total_classes": r.total_classes,
            "attended_classes": r.attended_classes,
            "attendance_percentage": round(percentage, 2)
        })

    return result


@app.put("/attendance/{attendance_id}", response_model=schemas.AttendanceResponse)
def update_attendance(
    attendance_id: int,
    attendance: schemas.AttendanceCreate,
    db: Session = Depends(get_db)
):
    record = db.query(models.Attendance).filter(
        models.Attendance.id == attendance_id
    ).first()

    if not record:
        raise HTTPException(status_code=404, detail="Attendance record not found")

    record.subject_id = attendance.subject_id
    record.total_classes = attendance.total_classes
    record.attended_classes = attendance.attended_classes

    db.commit()
    db.refresh(record)

    percentage = (
        record.attended_classes / record.total_classes * 100
        if record.total_classes > 0 else 0
    )

    return {
        "id": record.id,
        "subject_id": record.subject_id,
        "total_classes": record.total_classes,
        "attended_classes": record.attended_classes,
        "attendance_percentage": round(percentage, 2)
    }


@app.delete("/attendance/{attendance_id}")
def delete_attendance(attendance_id: int, db: Session = Depends(get_db)):
    record = db.query(models.Attendance).filter(
        models.Attendance.id == attendance_id
    ).first()

    if not record:
        raise HTTPException(status_code=404, detail="Attendance record not found")

    db.delete(record)
    db.commit()
    return {"message": "Attendance deleted successfully"}


# -------------------------
# DASHBOARD API
# -------------------------

@app.get("/dashboard", response_model=schemas.DashboardResponse)
def get_dashboard(db: Session = Depends(get_db)):

    total_subjects = db.query(models.Subject).count()

    total_tasks = db.query(models.Task).count()
    completed_tasks = db.query(models.Task).filter(
        models.Task.status == "Completed"
    ).count()
    pending_tasks = total_tasks - completed_tasks

    total_assignments = db.query(models.Assignment).count()
    pending_assignments = db.query(models.Assignment).filter(
        models.Assignment.status != "Submitted"
    ).count()

    attendance_records = db.query(models.Attendance).all()
    alerts = []

    for r in attendance_records:
        if r.total_classes > 0:
            percentage = (r.attended_classes / r.total_classes) * 100
            if percentage < 75:
                alerts.append(r.subject_id)

    return {
        "total_subjects": total_subjects,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "total_assignments": total_assignments,
        "pending_assignments": pending_assignments,
        "attendance_alerts": alerts
    }
