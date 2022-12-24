import logging

from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session

import app.main.schemas.Schemas
from app.main.database import get_db
from app.main.services import student_service, auth_service
from app.main.schemas import Schemas as schemas

router = APIRouter(prefix="/student",
                   tags=["student"],
                   dependencies=[Depends(auth_service.get_current_user)])


@router.get("/")
def get_all_students(first_name: str = None, last_name: str = None, sat_score_from: int = None,
                     sat_score_to: int = None, birthdate_from: str = None,
                     birthdate_to: str = None, orderby_field: str = 'graduation_score',
                     orderby_direction: str = 'asc', page: int = 0, count: int = 1):
    return student_service.get_all_students(first_name,
                                            last_name,
                                            sat_score_from,
                                            sat_score_to,
                                            birthdate_from,
                                            birthdate_to,
                                            orderby_field,
                                            orderby_direction,
                                            page,
                                            count)


# @router.get("/")
# def get_all_students(db: Session = Depends(get_db)):
#     return student_service.get_all_students(db)


@router.post("/",
             status_code=201,
             response_model=schemas.StudentDto,
             )
def create_student(req: app.main.schemas.Schemas.StudentDao, db: Session = Depends(get_db), current_user=Depends(auth_service.get_current_user)):
    student = student_service.save_new_student(db,
                                               req)

    return student_service.get_a_student(db,
                                         student.id)


@router.get("/{id}",
            response_model=schemas.StudentDto)
def get_a_student(id: int, db: Session = Depends(get_db)):
    return student_service.get_a_student(db,
                                         id)


@router.put("/{id}",
            response_model=schemas.StudentDto,
            status_code=200)
def update_student(id: int, req: schemas.StudentDao, db: Session = Depends(get_db)):
    return student_service.update_student(db,
                                          id,
                                          req)


@router.delete("/{id}",
               status_code=200,
               response_model=schemas.ResponseWithStatus)
def delete_student(id: int, db: Session = Depends(get_db)):
    return student_service.delete_a_student(db,
                                            id)


@router.post("/{studentId}/uploadFile")
async def upload_file(studentId: int, uploaded_file: UploadFile, db: Session = Depends(get_db)):
    if not uploaded_file:
        return {"error": "No file provided"}
    else:
        return student_service.upload_picture(db,
                                              studentId,
                                              uploaded_file.file)
