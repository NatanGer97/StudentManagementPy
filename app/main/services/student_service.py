from datetime import datetime
from typing import Dict, Tuple

from sqlalchemy.orm import Session

from app.main.model.models import Student
import app.main.model.models as models
from app.main.schemas.Schemas import StudentDao


def save_new_student(db: Session, req: StudentDao):
    # find student by email
    student = db.query(Student).filter(models.Student.email == req.email).first()

    if not student:
        new_student = Student(
            created_at=datetime.utcnow(),
            fullname=req.fullname,
            birthdate=req.birthdate,
            sat_score=req.sat_score,
            graduation_score=req.graduation_score,
            email=req.email,
            phone=req.phone,

        )
        save_changes(new_student,
                     db)
        # return the saved student

        return new_student

    else:
        response_object = {
            'status': 'fail',
            'message': 'Student already exists. ',
        }
        return response_object, 409


def update_student(db: Session, id: int, req: StudentDao):
    student = get_a_student(db,
                            id)

    if student:
        student.fullname = req.fullname
        student.birthdate = req.birthdate
        student.sat_score = req.sat_score
        student.graduation_score = req.graduation_score
        student.email = req.email
        student.phone = req.phone

        db.commit()

        # find the updated student & return it
        return get_a_student(db, id)


    else:
        response_object = {
            'status': 'fail',
            'message': 'Student does not exist. ',
        }
        return response_object, 404


def get_all_students(db: Session):
    return db.query(Student).all()


def get_a_student(db: Session, id: int):
    return db.query(Student).filter(models.Student.id == id).first()


def delete_a_student(db: Session, id: int):
    student = get_a_student(db,
                            id)

    if student:
        db.delete(student)
        db.commit()
        return {'message': 'Student deleted successfully',"status": "success"}

    else:
        response_object = {
            'status': 'fail',
            'message': 'Student does not exist. ',
        }
        return response_object


def save_changes(data: Student, db: Session):
    db.add(data)
    db.commit()
    db.refresh(data)
