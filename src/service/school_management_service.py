from src.service.dto import PopularDepartmentDTO, StudentsByGenderDTO, SchoolDepartmentDTO, StudentDTO
from src.database.repository import SchoolRepository, DepartmentRepository, StudentRepository
from src.domain.model import GenderEnum
from src.database.config import logger


class SchoolManagementService:
    """Service layer responsible for managing high-level school operations.

    This class coordinates interactions between repositories and converts
    ORM entities into Data Transfer Objects (DTOs) for use in higher layers
    of the application (e.g. API, UI).

    Attributes:
        school_repo (SchoolRepository): Repository handling `School` entities.
        department_repo (DepartmentRepository): Repository handling `Department` entities.
        student_repo (StudentRepository): Repository handling `Student` entities.
    """

    def __init__(
            self,
            school_repo: SchoolRepository,
            department_repo: DepartmentRepository,
            student_repo: StudentRepository
    ):
        """Initializes the SchoolManagementService with its required repositories.

        Args:
            school_repo (SchoolRepository): Repository for school data.
            department_repo (DepartmentRepository): Repository for department data.
            student_repo (StudentRepository): Repository for student data.
        """
        self.school_repo = school_repo
        self.department_repo = department_repo
        self.student_repo = student_repo

    def most_popular_department(self) -> list[PopularDepartmentDTO]:
        """Retrieves all departments sorted by student count (most popular first).

        Returns:
            list[PopularDepartmentDTO]: List of departments with student counts.
        """
        result: list[PopularDepartmentDTO] = []
        departments = self.department_repo.get_departments_with_student_count()
        if not departments:
            logger.info("No departments found")
        for d, count in departments:
            result.append(PopularDepartmentDTO.from_entity(d, count))
        return result

    def find_students_by_gender(self, gender: GenderEnum) -> list[StudentsByGenderDTO]:
        """Finds all students filtered by gender.

        Args:
            gender (GenderEnum): The gender to filter students by.

        Returns:
            list[StudentsByGenderDTO]: List of students matching the gender filter.
        """
        result: list[StudentsByGenderDTO] = []
        students = self.student_repo.get_students_by_gender(gender)
        if not students:
            logger.info("No students found")

        for student in students:
            result.append(StudentsByGenderDTO.from_entity(student))
        return result

    def schools_with_all_departments(self) -> list[SchoolDepartmentDTO]:
        """Retrieves all schools along with their related departments.

        Returns:
            list[SchoolDepartmentDTO]: List of schools including their departments.
        """
        result: list[SchoolDepartmentDTO] = []
        schools = self.school_repo.get_all_with_departments()
        if not schools:
            logger.info("No schools found")

        for school in schools:
            result.append(SchoolDepartmentDTO.from_entity(school))
        return result

    def find_student_between_age_range(self, age_min: int, age_max: int) -> list[StudentDTO]:
        """Finds students whose ages fall within a given range.

        Args:
            age_min (int): Minimum age (inclusive).
            age_max (int): Maximum age (inclusive).

        Returns:
            list[StudentDTO]: List of students whose ages are within the range.
        """
        result: list[StudentDTO] = []
        students = self.student_repo.get_student_age_between(age_min, age_max)
        if not students:
            logger.info("No students found")

        for student in students:
            result.append(StudentDTO.from_entity(student))
        return result

    def find_student_by_email(self, email: str) -> StudentDTO | None:
        """Finds a single student by their email address.

        Args:
            email (str): Email address of the student.

        Returns:
            StudentDTO | None: Student data if found, otherwise None.
        """
        students = self.student_repo.get_student_by_email(email)
        if not students:
            logger.info("No student found")
            return None
        return StudentDTO.from_entity(students)