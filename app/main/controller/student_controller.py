import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import app.main.schemas.Schemas
from app.main.database import get_db
from app.main.services import student_service
from app.main.schemas import Schemas as schemas

router = APIRouter(prefix="/student",
                   tags=["student"])


@router.get("/")
def get_all_students(db: Session = Depends(get_db)):
    return student_service.get_all_students(db)


@router.post("/",
             status_code=201, response_model=schemas.StudentDto
             )
def create_student(req: app.main.schemas.Schemas.StudentDao, db: Session = Depends(get_db)):
    student = student_service.save_new_student(db,
                                               req)
    return student_service.get_a_student(db,student.id)

@router.get("/{id}", response_model=schemas.StudentDto)
def get_a_student(id: int, db: Session = Depends(get_db)):
    return student_service.get_a_student(db, id)

@router.put("/{id}", response_model=schemas.StudentDto, status_code=200)
def update_student(id: int, req: schemas.StudentDao, db: Session = Depends(get_db)):
    return student_service.update_student(db, id, req)


@router.delete("/{id}", status_code=200, response_model=schemas.ResponseWithStatus)
def delete_student(id: int, db: Session = Depends(get_db)):
    return student_service.delete_a_student(db, id)

