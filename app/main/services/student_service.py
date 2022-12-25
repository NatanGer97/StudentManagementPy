import logging
from datetime import datetime
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.main.services.aws_service import upload_file, create_presigned_url
from app.main.util.fps import get_paginated
from app.main.model.models import Student
import app.main.model.models as models
from app.main.schemas.Schemas import StudentDao


def save_new_student(db: Session, req: StudentDao):
    # find student by email
    logging.info("save_new_student req: %s",
                 req.email)
    student = db.query(Student).filter(models.Student.email == req.email).first()

    if not student:
        new_student = Student(**req.dict())
        new_student.created_at = datetime.utcnow()
        # new_student = Student(
        #     created_at=datetime.utcnow(),
        #     first_name=req.first_name,
        #     last_name=req.last_name,
        #     birthdate=req.birthdate,
        #     sat_score=req.sat_score,
        #     graduation_score=req.graduation_score,
        #     email=req.email,
        #     phone=req.phone,
        #
        # )
        save_changes(new_student,
                     db)

        # return the saved student
        return new_student

    else:
        raise HTTPException(status_code=400,
                            detail="Student with given email already exists.")


def update_student(db: Session, id: int, req: StudentDao):
    student = get_a_student(db,
                            id)

    if student:

        student.first_name = req.first_name
        student.last_name = req.last_name
        student.birthdate = req.birthdate
        student.sat_score = req.sat_score
        student.graduation_score = req.graduation_score
        student.email = req.email
        student.phone = req.phone

        db.commit()

        # find the updated student & return it
        return get_a_student(db,
                             id)


    else:
        response_object = {
            'status': 'fail',
            'message': 'Student does not exist. ',
        }
        return response_object, 404


# def get_all_students(db: Session):
#     return db.query(Student).all()
def get_all_students(first_name, last_name, sat_score_from, sat_score_to, birthdate_from, birthdate_to, \
                     orderby_field, orderby_direction, page, count):
    fields = [
        ("s.id", "id"),
        ("s.created_at", "created_at"),
        ("s.first_name", "first_name"),
        ("s.last_name", "last_name"),
        # ("s.fullname", "fullname"),
        ("s.sat_score", "sat_score"),
        ("s.graduation_score", "graduation_score"),
        ("s.phone", "phone"),
        ("s.email", "email"),
        ("s.picture", "picture"),
        ("(select avg(sg.course_score) avg_score from  student_grade sg where sg.student_id = s.id ) ", "avg_score")
    ]
    from_str = " from students s "

    """and  s.first_name LIKE '%%' and s.last_name LIKE '%Gershbein%'''"""
    where_str = """ where (1=1) """
    if first_name is not None:
        where_str = where_str + " and s.first_name LIKE '%" + first_name + "%' "
        # where_str = where_str + " and (lower(first_name) LIKE   CONCAT('%', :first_name, '%'))"
    if last_name is not None:
        where_str = where_str + " and s.last_name LIKE '%" + last_name + "%' "
        # where_str = where_str + " and (lower(last_name) LIKE   CONCAT('%', :last_name, '%'))"
    if sat_score_from is not None:
        where_str = where_str + " and (sat_score  >=  :sat_score_from)"
    if sat_score_to is not None:
        where_str = where_str + " and (sat_score  <=  :sat_score_to)"
    if birthdate_from is not None:
        where_str = where_str + " and (birthdate  >=  :birthdate_from)"
    if birthdate_to is not None:
        where_str = where_str + " and (birthdate  <=  :birthdate_to)"

    params = {"first_name": first_name, "last_name": last_name, "sat_score_from": sat_score_from,
              "sat_score_to": sat_score_to,
              "birthdate_from": birthdate_from, "birthdate_to": birthdate_to}
    return get_paginated(fields=fields,
                         from_str=from_str,
                         where_str=where_str,
                         params=params,
                         orderby_field=orderby_field,
                         orderby_direction=orderby_direction,
                         page=page,
                         count=count)


def upload_picture(db: Session, student_id: int, picture):
    student = get_a_student(db,
                            student_id)

    if student:
        student.picture = "apps/python/student-" + str(student_id) + ".png"
        upload_file(picture,
                    student.picture)
        db.commit()

        return {'message': 'Student picture uploaded successfully', "status": "success"}

    else:
        response_object = {
            'status': 'fail',
            'message': 'Student does not exist. ',
        }
        return response_object


def get_a_student(db: Session, id: int):
    student = db.query(Student).filter(models.Student.id == id).first()

    if student.picture:
        student.picture = create_presigned_url(student.picture)
        return student
    elif student:
        return student
    # if student:
    #     if student.picture is not None:
    #         student.picture = create_presigned_url(student.picture)
    #     return student
    else:
        raise HTTPException(status_code=404,
                            detail="Student not found")


def delete_a_student(db: Session, id: int):
    student = get_a_student(db,
                            id)

    if student:
        db.delete(student)
        db.commit()
        return {'message': 'Student deleted successfully', "status": "success"}

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
