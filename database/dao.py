from typing import List

from sqlalchemy import create_engine
from sqlalchemy import String, DateTime, Boolean, BigInteger, ForeignKey, Integer, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, Session, relationship, DeclarativeBase
from sqlalchemy.sql import func
import os

"""
Setup

Entities

Session
Session dirty
Delete
Flush
Rollback

Select
Select with filter
Select where
Select filter
Select specific column




relationship

"""



class Base(DeclarativeBase):
    def to_dict(self):
        """Return a dictionary representation of this model."""
        ret_data = {}
        columns = self.__table__.columns.keys()
        for c in columns:
            ret_data[c] = getattr(self, c)
        return ret_data


semester_student = Table(
    "semester_student",
    Base.metadata,
    Column("left_id", ForeignKey("semester.id"), primary_key=True),
    Column("right_id", ForeignKey("student.id"), primary_key=True),
)

class Semester(Base):
    __tablename__ = "semester"
    id: Mapped[int] = mapped_column(primary_key=True)
    season: Mapped[str] = mapped_column(String)
    start_date: Mapped[str] = mapped_column(String)
    end_date: Mapped[str] = mapped_column(String)
    students: Mapped[List["Student"]] = relationship(secondary=semester_student, back_populates="semesters")


class Student(Base):
    __tablename__ = "student"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    semesters: Mapped[List["Semester"]] = relationship(secondary=semester_student, back_populates="students")


engine = create_engine("sqlite:///app.db")
session = Session(engine)

if not os.path.exists('app1.db'):
    Base.metadata.create_all(engine)