from typing import List

from sqlalchemy import create_engine
from sqlalchemy import String, DateTime, Boolean, BigInteger, ForeignKey, Integer, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, Session, relationship, DeclarativeBase
from sqlalchemy.sql import func
import os


class Base(DeclarativeBase):
    def to_dict(self):
        """Return a dictionary representation of this model."""
        ret_data = {}
        columns = self.__table__.columns.keys()
        for c in columns:
            ret_data[c] = getattr(self, c)
        return ret_data


course_user = Table(
    "course_user",
    Base.metadata,
    Column("left_id", ForeignKey("course.id"), primary_key=True),
    Column("right_id", ForeignKey("user.id"), primary_key=True),
)

semester_course = Table(
    "semester_course",
    Base.metadata,
    Column("left_id", ForeignKey("semester.id"), primary_key=True),
    Column("right_id", ForeignKey("course.id"), primary_key=True),
)

program_course = Table(
    "program_course",
    Base.metadata,
    Column("left_id", ForeignKey("program.id"), primary_key=True),
    Column("right_id", ForeignKey("course.id"), primary_key=True),
)

class Semester(Base):
    __tablename__ = "semester"
    id: Mapped[int] = mapped_column(primary_key=True)
    season: Mapped[str] = mapped_column(String)
    start_date: Mapped[str] = mapped_column(String)
    end_date: Mapped[str] = mapped_column(String)
    courses: Mapped[List["Course"]] = relationship(secondary=semester_course, back_populates="semesters")


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    role: Mapped[str] = mapped_column(String)
    program_id: Mapped[int] = mapped_column(ForeignKey("program.id"))
    program: Mapped["Program"] = relationship(back_populates="users")
    active: Mapped[bool] = mapped_column(Boolean)
    courses: Mapped[List["Course"]] = relationship(secondary=course_user, back_populates="users")

class Course(Base):
    __tablename__ = "course"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    total_hours: Mapped[int] = mapped_column(Integer)
    users: Mapped[List["User"]] = relationship(secondary=course_user, back_populates="courses")
    semesters: Mapped[List["Semester"]] = relationship(secondary=semester_course, back_populates="courses")
    programs: Mapped[List["Program"]] = relationship(secondary=program_course, back_populates="courses")

class Program(Base):
    __tablename__ = "program"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    total_hours: Mapped[int] = mapped_column(Integer)
    users: Mapped[List["User"]] = relationship(back_populates="program")
    courses: Mapped[List["Course"]] = relationship(secondary=program_course, back_populates="programs")

def db_reset():
    Base.metadata.drop_all(engine)

engine = create_engine("sqlite:///app.db")
session = Session(engine)

if not os.path.exists('app.db'):
    Base.metadata.create_all(engine)