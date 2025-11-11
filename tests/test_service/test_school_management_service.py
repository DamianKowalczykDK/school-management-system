import logging
from unittest.mock import MagicMock
import pytest

from src.database.repository import DepartmentRepository
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
        mock_school_management_service.find_student_by_email('js@example.com')

    assert 'No student found' in caplog.text

def test_add_school(
        mock_school_repository: MagicMock,
        mock_school_management_service: SchoolManagementService
) -> None:

    mock_school_repository.find_by_name.return_value = None
    mock_school_repository.save.return_value = None
    mock_school_management_service.add_school('Test School')

    mock_school_repository.save.assert_called_once()

def test_add_school_if_school_exist(
        mock_school_repository: MagicMock,
        mock_school_management_service: SchoolManagementService
) -> None:

    with pytest.raises(ValueError, match='School already exists'):
        mock_school_repository.find_by_name.return_value = 'Test School'
        mock_school_repository.save.return_value = 'Test School'
        mock_school_management_service.add_school('Test School')

def test_add_department_to_school(
        mock_school_repository: MagicMock,
        mock_department_repository: MagicMock,
        mock_school_management_service: SchoolManagementService,
        school_1: School
) -> None:
        mock_school_repository.find_by_name.return_value = school_1
        mock_department_repository.get_find_by_name.return_value = None
        mock_department_repository.save.return_value = None

        mock_school_management_service.add_department_to_school(school_1.name, 'Test Department')
        mock_department_repository.save.assert_called_once()


def test_add_department_to_school_if_school_not_exist(
        mock_school_repository: MagicMock,
        mock_department_repository: MagicMock,
        mock_school_management_service: SchoolManagementService,
 ) -> None:
        with pytest.raises(ValueError, match='School does not exist'):
            mock_school_repository.find_by_name.return_value = None
            mock_school_repository.save.return_value = None
            mock_department_repository.get_find_by_name.return_value = None
            mock_department_repository.save.return_value = None

            mock_school_management_service.add_department_to_school('Test School', 'Test Department')


def test_add_department_to_school_if_department_exist(
        mock_school_repository: MagicMock,
        mock_department_repository: MagicMock,
        mock_school_management_service: SchoolManagementService,
        school_1: School,
        department_1: Department
) -> None:
    with pytest.raises(ValueError, match='Department already exists'):
        mock_school_repository.find_by_name.return_value = school_1
        mock_department_repository.get_find_by_name.return_value = department_1


        mock_school_management_service.add_department_to_school(school_1.name, department_1.name)

def test_add_student_to_school(
        mock_school_repository: MagicMock,
        mock_department_repository: MagicMock,
        mock_student_repository: MagicMock,
        mock_school_management_service: SchoolManagementService,
        school_1: School,
        department_1: Department,
  ) -> None:
    mock_school_repository.find_by_name.return_value = school_1
    mock_department_repository.get_find_by_name.return_value = department_1
    mock_student_repository.get_student_by_department.return_value = None
    mock_student_repository.save.return_value = None

    mock_school_management_service.add_student_to_school(
        school=school_1.name,
        department=department_1.name,
        first_name='Test Name',
        last_name='Test Name',
        gender=GenderEnum.MALE,
        age=20,
        email='test@.test.com'
    )

    mock_student_repository.save.assert_called_once()

def test_add_student_to_school_if_school_not_exist(
        mock_school_repository: MagicMock,
        mock_school_management_service: SchoolManagementService,
        school_1: School,
        department_1: Department,
  ) -> None:
    with pytest.raises(ValueError, match='School does not exist'):
        mock_school_repository.find_by_name.return_value = None
        mock_school_repository.save.return_value = None


        mock_school_management_service.add_student_to_school(
            school=school_1.name,
            department=department_1.name,
            first_name='Test Name',
            last_name='Test Name',
            gender=GenderEnum.MALE,
            age=20,
            email='test@.test.com'
        )

def test_add_student_to_school_if_department_is_none(
        mock_school_repository: MagicMock,
        mock_department_repository: MagicMock,
        mock_school_management_service: SchoolManagementService,
        school_1: School,
        department_1: Department,
  ) -> None:
    with pytest.raises(ValueError, match='Department does not exist'):
        mock_school_repository.find_by_name.return_value = school_1
        mock_department_repository.get_find_by_name.return_value = None

        mock_school_management_service.add_student_to_school(
            school=school_1.name,
            department=department_1.name,
            first_name='Test Name',
            last_name='Test Name',
            gender=GenderEnum.MALE,
            age=20,
            email='test@.test.com'
        )

def test_add_student_to_school_if_student_exist(
        mock_school_repository: MagicMock,
        mock_department_repository: MagicMock,
        mock_student_repository: MagicMock,
        mock_school_management_service: SchoolManagementService,
        school_1: School,
        department_1: Department,
        student_1: Student
  ) -> None:
    with pytest.raises(ValueError, match='Student already exists'):
        mock_school_repository.find_by_name.return_value = school_1
        mock_department_repository.get_find_by_name.return_value = department_1
        mock_student_repository.get_student_by_department.return_value = student_1

        mock_school_management_service.add_student_to_school(
            school=school_1.name,
            department=department_1.name,
            first_name=student_1.first_name,
            last_name=student_1.last_name,
            gender=student_1.gender,
            age=student_1.age,
            email=student_1.email
        )




