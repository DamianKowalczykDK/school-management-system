import logging
from unittest.mock import MagicMock
import pytest
from src.domain.model import Department, Student, GenderEnum, School
from src.service.school_management_service import SchoolManagementService


def test_most_popular_department(
        mock_department_repository: MagicMock,
        mock_school_management_service: SchoolManagementService,
        department_1: Department
) -> None:
    mock_department_repository.get_departments_with_student_count.return_value = [(department_1, 1)]

    result = mock_school_management_service.most_popular_department()
    assert len(result) == 1
    assert result[0].name == department_1.name
    assert result[0].student_count == 1

def test_most_popular_department_if_not_departments(
        mock_department_repository: MagicMock,
        mock_school_management_service: SchoolManagementService,
        caplog: pytest.LogCaptureFixture
) -> None:
    with caplog.at_level(logging.INFO):
        mock_department_repository.get_departments_with_student_count.return_value = []
        result = mock_school_management_service.most_popular_department()

    assert len(result) == 0
    assert 'No departments found' in caplog.text


def test_find_students_by_gender(
        mock_student_repository: MagicMock,
        mock_school_management_service: SchoolManagementService,
        student_1: Student
) -> None:

    mock_student_repository.get_students_by_gender.return_value = [student_1]

    result = mock_school_management_service.find_students_by_gender(gender=GenderEnum.MALE)
    assert len(result) == 1
    assert result[0].gender == GenderEnum.MALE

def test_find_student_by_gender_if_not_students(
        mock_student_repository: MagicMock,
        mock_school_management_service: SchoolManagementService,
        caplog: pytest.LogCaptureFixture
) -> None:
    with caplog.at_level(logging.INFO):
        mock_student_repository.get_students_by_gender.return_value = []
        result = mock_school_management_service.find_students_by_gender(gender=GenderEnum.FEMALE)

    assert len(result) == 0
    assert 'No students found' in caplog.text

def test_schools_with_all_departments(
        mock_school_repository: MagicMock,
        mock_school_management_service: SchoolManagementService,
        school_1: School,
) -> None:

    mock_school_repository.get_all_with_departments.return_value = [school_1]
    result = mock_school_management_service.schools_with_all_departments()
    assert len(result) == 1
    assert result[0].name == school_1.name
    assert result[0].department == school_1.departments

def test_schools_with_all_departments_if_not_schools(
        mock_school_repository: MagicMock,
        mock_school_management_service: SchoolManagementService,
        caplog: pytest.LogCaptureFixture
) -> None:
    with caplog.at_level(logging.INFO):
        mock_school_repository.get_all_with_departments.return_value = []
        result = mock_school_management_service.schools_with_all_departments()

    assert len(result) == 0
    assert 'No schools found' in caplog.text

def test_find_student_between_age_range(
        mock_student_repository: MagicMock,
        mock_school_management_service: SchoolManagementService,
        student_1: Student
) -> None:
    mock_student_repository.get_student_age_between.return_value = [student_1]
    result = mock_school_management_service.find_student_between_age_range(18, 22)
    assert result is not None
    assert len(result) == 1
    assert result[0].age == student_1.age

def test_find_student_between_age_range_if_not_students(
        mock_student_repository: MagicMock,
        mock_school_management_service: SchoolManagementService,
        caplog: pytest.LogCaptureFixture
) -> None:
    with caplog.at_level(logging.INFO):
        mock_student_repository.get_student_age_between.return_value = []
        result = mock_school_management_service.find_student_between_age_range(18, 22)

    assert len(result) == 0
    assert 'No students found' in caplog.text

def test_find_student_by_email(
        mock_student_repository: MagicMock,
        mock_school_management_service: SchoolManagementService,
        student_1: Student
) -> None:
    mock_student_repository.get_student_by_email.return_value = student_1

    result = mock_school_management_service.find_student_by_email('js@example.com')

    assert result is not None
    assert result.email == student_1.email

def test_find_student_by_email_if_not_student(
        mock_student_repository: MagicMock,
        mock_school_management_service: SchoolManagementService,
        caplog: pytest.LogCaptureFixture
) -> None:
    with caplog.at_level(logging.INFO):
        mock_student_repository.get_student_by_email.return_value = None
        result = mock_school_management_service.find_student_by_email('js@example.com')

    assert 'No student found' in caplog.text



