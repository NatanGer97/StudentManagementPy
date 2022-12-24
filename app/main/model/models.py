import sqlalchemy
from sqlalchemy import Column, Integer, DateTime, String

from ..database import  Base


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False)
    # fullname = Column(String(100), unique=False, nullable=False)
    first_name = Column(String(100), unique=False, nullable=False)
    last_name = Column(String(100), unique=False, nullable=False)
    birthdate = Column(sqlalchemy.Date, nullable=True)
    sat_score = Column(Integer, nullable=True)
    graduation_score = Column(sqlalchemy.Float, nullable=True)
    email = Column(String(255), unique=False, nullable=True)
    phone = Column(String(20), unique=False, nullable=True)
    picture = Column(String(300), unique=False, nullable=True)

    def __repr__(self):
        return f"Student(id={self.id}, fullname={self.fullname}, email={self.email})"

class StudentGrade(Base):
    __tablename__ = 'student_grade'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime, nullable=False)
    student_id = Column(Integer, nullable=False)
    course_name = Column(String(100), unique=False, nullable=False)
    course_score = Column(Integer, nullable=True)

    def __repr__(self):
        return f"StudentGrade(id={self.id}, student_id={self.student_id}, course_name={self.course_name}, course_score={self.course_score})"

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(sqlalchemy.Boolean, default=True)
    username = Column(String(255), unique=True, nullable=False)

    def __repr__(self):
        return f"User(id={self.id}, email={self.email}, is_active={self.is_active})"