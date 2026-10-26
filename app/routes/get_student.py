from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Student
from app.schemas import StudentRead

router = APIRouter()

@router.get("/students", response_model=list[StudentRead])
def list_students(
    name: Optional[str] = Query(default=None, description="Case-insensitive partial name match"),
    course: Optional[str] = Query(default=None, description="Case-insensitive partial course match"),
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    statement = select(Student)
    if name:
        statement = statement.where(Student.name.ilike(f"%{name}%"))
    if course:
        statement = statement.where(Student.course.ilike(f"%{course}%"))
    statement = statement.order_by(Student.id).offset(offset).limit(limit)
    return list(db.scalars(statement).all())

@router.get("/students/{student_id}", response_model=StudentRead)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found.")
    return student
