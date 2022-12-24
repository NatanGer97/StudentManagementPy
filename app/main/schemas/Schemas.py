import datetime

from pydantic import BaseModel
from sqlalchemy import DateTime


class StudentDao(BaseModel):
    # fullname: str
    first_name: str
    last_name: str
    birthdate: datetime.date
    # birthdate: datetime.datetime
    sat_score: int
    graduation_score: float
    email: str
    phone: str


class StudentDto(BaseModel):
    id: int
    created_at: datetime.datetime
    # fullname: str
    first_name: str
    last_name: str
    birthdate: datetime.date
    # birthdate: datetime.datetime
    sat_score: int
    graduation_score: float
    email: str
    phone: str

    class Config:
        orm_mode = True


class StudentGradeDao(BaseModel):
    course_name: str
    course_score: int

class StudentGradeDto(BaseModel):
    id: int
    created_at: datetime.date
    student_id: int
    course_name: str
    course_score: int

    class Config:
        orm_mode = True


class ResponseWithStatus(BaseModel):
    message: str
    status: str

    class Config:
        orm_mode = True
