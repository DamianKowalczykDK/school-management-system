from src.domain.model import Department, GenderEnum, Student, School
from dataclasses import dataclass
from typing import Self


@dataclass
class PopularDepartmentDTO:
    """Data Transfer Object (DTO) representing a popular department.

    Attributes:
        name (str): The name of the department.
        student_count (int): Number of students enrolled in the department.
    """

    name: str
    student_count: int

    @classmethod
    def from_entity(cls, department: Department, student_count: int) -> Self:
        """Creates a PopularDepartmentDTO from a Department entity.

        Args:
            department (Department): Department entity instance.
            student_count (int): Number of students in the department.

        Returns:
            PopularDepartmentDTO: DTO with department name and student count.
        """
        return cls(
            name=department.name,
            student_count=student_count
        )


@dataclass
class StudentsByGenderDTO:
    """DTO representing a student's personal information grouped by gender.

    Attributes:
        first_name (str): Student's first name.
        last_name (str): Student's last name.
        gender (GenderEnum): Gender of the student.
        age (int): Age of the student.
        email (str): Email address of the student.
    """

    first_name: str
    last_name: str
    gender: GenderEnum
    age: int
    email: str

    @classmethod
    def from_entity(cls, student: Student) -> Self:
        """Creates a StudentsByGenderDTO from a Student entity.

        Args:
            student (Student): Student entity instance.

        Returns:
            StudentsByGenderDTO: DTO with student details.
        """
        return cls(
            first_name=student.first_name,
            last_name=student.last_name,
            gender=GenderEnum(student.gender),
            age=student.age,
            email=student.email
        )


@dataclass
class SchoolDepartmentDTO:
    """DTO representing a school with its departments.

    Attributes:
        name (str): Name of the school.
        department (list[Department]): List of department entities belonging to the school.
    """

    name: str
    department: list[Department]

    @classmethod
    def from_entity(cls, school: School) -> Self:
        """Creates a SchoolDepartmentDTO from a School entity.

        Args:
            school (School): School entity instance.

        Returns:
            SchoolDepartmentDTO: DTO with school name and department list.
        """
        return cls(
            name=school.name,
            department=school.departments
        )


@dataclass
class StudentDTO:
    """DTO representing essential student information.

    Attributes:
        first_name (str): Student's first name.
        last_name (str): Student's last name.
        age (int): Age of the student.
        gender (GenderEnum): Gender of the student.
        email (str): Email address of the student.
    """

    first_name: str
    last_name: str
    age: int
    gender: GenderEnum
    email: str

    @classmethod
    def from_entity(cls, student: Student) -> Self:
        """Creates a StudentDTO from a Student entity.

        Args:
            student (Student): Student entity instance.

        Returns:
            StudentDTO: DTO containing key student information.
        """
        return cls(
            first_name=student.first_name,
            last_name=student.last_name,
            gender=GenderEnum(student.gender),
            age=student.age,
            email=student.email
        )