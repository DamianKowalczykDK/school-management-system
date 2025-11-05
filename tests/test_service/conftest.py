from unittest.mock import MagicMock

import pytest

from src.database.repository import SchoolRepository, DepartmentRepository, StudentRepository
from src.service.school_management_service import SchoolManagementService


@pytest.fixture
def mock_school_repository() -> MagicMock:
    return MagicMock(spec=SchoolRepository)

@pytest.fixture
def mock_department_repository() -> MagicMock:
    return MagicMock(spec=DepartmentRepository)

@pytest.fixture
def mock_student_repository() -> MagicMock:
    return MagicMock(spec=StudentRepository)

@pytest.fixture
def mock_school_management_service(
        mock_school_repository: MagicMock,
        mock_department_repository: MagicMock,
        mock_student_repository: MagicMock
) -> SchoolManagementService:
    return SchoolManagementService(
        school_repo=mock_school_repository,
        department_repo=mock_department_repository,
        student_repo=mock_student_repository,
    )
