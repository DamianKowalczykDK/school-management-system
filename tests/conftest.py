from src.domain.model import School, Department, Student, GenderEnum
from testcontainers.mysql import MySqlContainer  # type: ignore
import pytest

@pytest.fixture
def school_1() -> School:
    return School(name='Harvard University')

@pytest.fixture
def school_2() -> School:
    return School(name='Oxford University')

@pytest.fixture
def department_1(school_1: School) -> Department:
    return Department(name='Biology', school=school_1)

@pytest.fixture
def student_1(department_1: Department) -> Student:
    return Student(
        first_name='Jon',
        last_name='Smith',
        gender=GenderEnum.MALE,
        age=20,email='js@example.com',
        department=department_1
    )
