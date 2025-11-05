from src.database.repository import SchoolRepository, DepartmentRepository, StudentRepository
from src.domain.model import GenderEnum, School
from src.service.dto import PopularDepartmentDTO, StudentsByGenderDTO, SchoolDepartmentDTO, StudentDTO
from src.database.config import logger


class SchoolManagementService:
    def __init__(
            self,
            school_repo: SchoolRepository,
            department_repo: DepartmentRepository,
            student_repo: StudentRepository
    ):
        self.school_repo = school_repo
        self.department_repo = department_repo
        self.student_repo = student_repo

    def most_popular_department(self) -> list[PopularDepartmentDTO] :
        result: list[PopularDepartmentDTO] = []
        departments = self.department_repo.get_departments_with_student_count()
        if not departments:
            logger.info("No departments found")
        for d, count in departments:
            result.append(PopularDepartmentDTO.from_entity(d, count))
        return result

    def find_students_by_gender(self, gender: GenderEnum) -> list[StudentsByGenderDTO]:
        result: list[StudentsByGenderDTO] = []
        students = self.student_repo.get_students_by_gender(gender)
        if not students:
            logger.info("No students found")

        for student in students:
            result.append(StudentsByGenderDTO.from_entity(student))
        return result

    def schools_with_all_departments(self) -> list[SchoolDepartmentDTO]:
        result: list[SchoolDepartmentDTO] = []
        schools = self.school_repo.get_all_with_departments()
        if not schools:
            logger.info("No schools found")

        for school in schools:
            result.append(SchoolDepartmentDTO.from_entity(school))
        return result

    def find_student_between_age_range(self, age_min: int, age_max: int) -> list[StudentDTO]:
        result: list[StudentDTO] = []
        students = self.student_repo.get_student_age_between(age_min, age_max)
        if not students:
            logger.info("No students found")

        for student in students:
            result.append(StudentDTO.from_entity(student))
        return result

    def find_student_by_email(self, email: str) -> StudentDTO | None:
        students = self.student_repo.get_student_by_email(email)
        if not students:
            logger.info("No student found")
            return None
        return StudentDTO.from_entity(students)




