import sqlalchemy
from sqlalchemy import Column, Integer, DateTime, String

from ..database import  Base


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False)
    fullname = Column(String(100), unique=False, nullable=False)
    birthdate = Column(DateTime, nullable=True)
    sat_score = Column(Integer, nullable=True)
    graduation_score = Column(sqlalchemy.Float, nullable=True)
    email = Column(String(255), unique=False, nullable=True)
    phone = Column(String(20), unique=False, nullable=True)
    picture = Column(String(300), unique=False, nullable=True)

    def __repr__(self):
        return f"Student(id={self.id}, fullname={self.fullname}, email={self.email})"