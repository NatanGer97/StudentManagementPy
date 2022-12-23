import datetime

from pydantic import BaseModel
from sqlalchemy import DateTime


class StudentDao(BaseModel):
    fullname: str
    birthdate: datetime.datetime
    sat_score: int
    graduation_score: float
    email: str
    phone: str


class StudentDto(BaseModel):
    id: int
    created_at: datetime.datetime
    fullname: str
    birthdate: datetime.datetime
    sat_score: int
    graduation_score: float
    email: str
    phone: str

    class Config:
        orm_mode = True


class ResponseWithStatus(BaseModel):
    message: str
    status: str

    class Config:
        orm_mode = True
