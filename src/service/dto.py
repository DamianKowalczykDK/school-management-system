from dataclasses import dataclass
from typing import Self

from src.domain.model import Department, GenderEnum, Student, School


@dataclass
class PopularDepartmentDTO:
    name: str
    student_count: int

    @classmethod
    def from_entity(cls, department: Department, student_count:int) -> Self:
        return cls(
            name=department.name,
            student_count=student_count
        )
@dataclass
class StudentsByGenderDTO:
    first_name: str
    last_name: str
    gender: GenderEnum
    age: int
    email: str

    @classmethod
    def from_entity(cls, student: Student) -> Self:
        return cls(
            first_name=student.first_name,
            last_name=student.last_name,
            gender=GenderEnum(student.gender),
            age=student.age,
            email=student.email
        )

@dataclass
class SchoolDepartmentDTO:
    name: str
    department: list[Department]


    @classmethod
    def from_entity(cls, school: School) -> Self:
        return cls(
            name=school.name,
            department=school.departments
        )

@dataclass
class StudentDTO:
    first_name: str
    last_name: str
    age: int
    gender: GenderEnum
    email: str
    @classmethod
    def from_entity(cls, student: Student) -> Self:
        return cls(
            first_name=student.first_name,
            last_name=student.last_name,
            gender=GenderEnum(student.gender),
            age=student.age,
            email=student.email
        )