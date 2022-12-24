from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.main.model.models import Student, StudentGrade
from app.main.schemas.Schemas import StudentGradeDao


def save_new_student_grade(db: Session, req: StudentGradeDao, student_id: int):
    student = db.query(Student).filter(Student.id == student_id).first()
    if (student):
        new_student_grade = StudentGrade(
            created_at=datetime.utcnow(),
            student_id=student_id,
            course_name=req.course_name,
            course_score=req.course_score
        )

        save_changes(new_student_grade,db)
        return {"status": "success", "message": "Student grade saved successfully.", "data": new_student_grade, "status_code": 201}
    else:
        raise HTTPException(status_code=400, detail="Student with given id does not exist.")
        response_object = {
            'status': 'fail',
            'message': 'Student does not exist. ',
            "status_code": 404
        }

        return response_object

def update_student_grade(db: Session, id: int, req: StudentGradeDao):
    student_grade = db.query(StudentGrade).filter(StudentGrade.id == id).first()
    if student_grade:
        student_grade.course_name = req.course_name
        student_grade.course_score = req.course_score
        db.commit()
        return {"status": "success", "message": "Student grade updated successfully.", "data": student_grade.course_name, "status_code": 200}
    else:
        raise HTTPException(status_code=400, detail="Student grade with given id does not exist.")
        response_object = {
            'status': 'fail',
            'message': 'Student grade does not exist. ',
            "status_code": 404
        }
        return response_object


def get_all_student_grades(db: Session, student_id: int):
    if db.query(Student).filter(Student.id == student_id).first():
        return db.query(StudentGrade).filter(StudentGrade.student_id == student_id).all()
    else:
        raise HTTPException(status_code=400, detail="Student with given id does not exist.")


def delete_a_student_grade(db: Session, grade_id: int):
    student_grade = db.query(StudentGrade).filter(StudentGrade.id == grade_id).first()
    if student_grade:
        db.delete(student_grade)
        db.commit()
        return {"status": "success", "message": "Student grade deleted successfully.", "status_code": 200}
    else:
        raise HTTPException(status_code=400, detail="Student grade with given id does not exist.")
        response_object = {
            'status': 'fail',
            'message': 'Student grade does not exist. ',
            "status_code": 404
        }
        return response_object


def save_changes(data, db: Session):
    db.add(data)
    db.commit()
    db.refresh(data)
