from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Student
from app.schemas import StudentRead, StudentUpdate

router = APIRouter()

@router.put("/students/{student_id}", response_model=StudentRead)
def update_student(student_id: int, payload: StudentUpdate, db: Session = Depends(get_db)):
    student = db.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found.")

    changes = payload.model_dump(exclude_unset=True)
    if not changes:
        raise HTTPException(status_code=422, detail="Provide at least one field to update.")

    for field, value in changes.items():
        setattr(student, field, value)

    # If the client explicitly clears both contact fields, reject the update.
    if not student.email and not student.phone:
        db.rollback()
        raise HTTPException(status_code=422, detail="A student must have an email or phone number.")

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="A student with this email already exists.")
    db.refresh(student)
    return student

@router.patch("/students/{student_id}", response_model=StudentRead, include_in_schema=True)
def patch_student(student_id: int, payload: StudentUpdate, db: Session = Depends(get_db)):
    return update_student(student_id, payload, db)
