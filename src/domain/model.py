from sqlalchemy import ForeignKey, Integer, String, Enum as SAEnum
from sqlalchemy.orm import relationship, mapped_column, Mapped
from src.database.config import Base
from enum import Enum


class GenderEnum(Enum):
    """Enumeration representing possible genders of a student."""

    MALE = 'Male'
    FEMALE = 'Female'


class School(Base):
    """Represents a school entity in the database.

    Attributes:
        id (int): Primary key identifier of the school.
        name (str): Name of the school.
        departments (list[Department]): List of departments belonging to this school.
    """

    __tablename__ = 'schools'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    departments: Mapped[list['Department']] = relationship(back_populates='school', lazy='select')

    def __repr__(self) -> str:
        """Returns a string representation of the school.

        Returns:
            str: String with the school name.
        """
        return f'School({self.name})'


class Department(Base):
    """Represents a department entity in the database.

    Attributes:
        id (int): Primary key identifier of the department.
        name (str): Department name.
        school_id (int): Foreign key referencing the school this department belongs to.
        school (School): Relationship to the associated school.
        students (list[Student]): List of students assigned to this department.
    """

    __tablename__ = 'departments'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    school_id: Mapped[int] = mapped_column(Integer, ForeignKey('schools.id'), nullable=False)
    school: Mapped[School] = relationship(back_populates='departments')
    students: Mapped[list['Student']] = relationship(back_populates='department', lazy='select')

    def __repr__(self) -> str:
        """Returns a string representation of the department.

        Returns:
            str: String with the department name.
        """
        return f'Department: {self.name}'


class Student(Base):
    """Represents a student entity in the database.

    Attributes:
        id (int): Primary key identifier of the student.
        first_name (str): Student's first name.
        last_name (str): Student's last name.
        gender (GenderEnum): Gender of the student.
        age (int): Age of the student.
        email (str): Student's email address.
        department_id (int): Foreign key referencing the department this student belongs to.
        department (Department): Relationship to the associated department.
    """

    __tablename__ = 'students'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    gender: Mapped[GenderEnum] = mapped_column(SAEnum(GenderEnum), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False)

    department_id: Mapped[int] = mapped_column(Integer, ForeignKey('departments.id'), nullable=False)
    department: Mapped[Department] = relationship(back_populates='students', lazy='select')

    def __repr__(self) -> str:
        """Returns a string representation of the student with key attributes.

        Returns:
            str: Human-readable string describing the student.
        """
        return f'Student: {self.first_name} {self.last_name} {self.gender} {self.age} {self.email}'
