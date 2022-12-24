import datetime
from typing import List

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
    first_name: str
    last_name: str
    birthdate: datetime.date
    sat_score: int
    graduation_score: float
    email: str
    phone: str
    picture: str

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



class EmailDao(BaseModel):
    recipient: str
    subject: str
    content: str

    class Config:
        orm_mode = True

class EmailBody(BaseModel):
    title: str
    content: str
    btn_text: str
    btn_url: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str
    email: str
    disabled: bool = None

class UserIn(User):
    password: str

class UserInDB(User):
    hashed_password: str








