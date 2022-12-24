from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import app.main.schemas.Schemas as schemas
from app.main.database import get_db
from app.main.services import student_grade_service, auth_service

router = APIRouter(prefix="/grades", tags=["grades"],
                   dependencies=[Depends(auth_service.get_current_user)])

@router.get("/{student_id}/grade",  status_code=200)
def get_student_grade(student_id: int, db: Session = Depends(get_db)):
    return student_grade_service.get_all_student_grades(db, student_id)

@router.post("/{student_id}/grade",  status_code=201)
def create_student_grade(student_id: int, req: schemas.StudentGradeDao, db: Session = Depends(get_db)):
    return student_grade_service.save_new_student_grade(db, req, student_id)

@router.get("/{student_id}/grade",  status_code=200)
def get_student_grade(student_id: int, db: Session = Depends(get_db)):
    return student_grade_service.get_all_student_grades(db, student_id)

@router.put("/{student_id}/grade/{grade_id}",  status_code=200)
def update_student_grade(student_id: int, grade_id: int, req: schemas.StudentGradeDao, db: Session = Depends(get_db)):
    return student_grade_service.update_student_grade(db, grade_id, req)

@router.delete("/{student_id}/grade/{grade_id}",  status_code=200)
def delete_student_grade(student_id: int, grade_id: int, db: Session = Depends(get_db)):
    return student_grade_service.delete_a_student_grade(db, grade_id)
