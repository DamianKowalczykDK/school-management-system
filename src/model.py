from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy import ForeignKey, Integer, String
from src.db.config import Base



class School(Base):
    __tablename__ = 'schools'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    departments: Mapped[list['Department']] = relationship(back_populates='school', lazy='select')

class Department(Base):
    __tablename__ = 'departments'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    school_id: Mapped[int] = mapped_column(Integer, ForeignKey('schools.id'), nullable=False)
    school: Mapped[School] = relationship(back_populates='departments')
    students: Mapped[list['Student']] = relationship(back_populates='department', lazy='select')

class Student(Base):
    __tablename__ = 'students'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    gender: Mapped[str] = mapped_column(String(10), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False)

    school_id: Mapped[int] = mapped_column(Integer, ForeignKey('schools.id'), nullable=False)
    department_id: Mapped[int] = mapped_column(Integer, ForeignKey('departments.id'), nullable=False)

    department: Mapped[Department] = relationship(back_populates='students', lazy='select')



