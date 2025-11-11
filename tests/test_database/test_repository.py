from src.database.repository import SchoolRepository, GenericRepository, DepartmentRepository, StudentRepository
from src.domain.model import School, Department, Student, GenderEnum
from sqlalchemy import Engine, text
from sqlalchemy.orm import Session
import pytest

class TestGenericRepository:
    def test_school_save(self, school_repo: SchoolRepository, db_session: Session, school_1: School) -> None:
        school_repo.save(school_1, db_session)
        db_session.flush()

        found_school = school_repo.find_by_id(school_1.id, db_session)
        assert found_school is not None
        assert found_school.name == school_1.name
        assert repr(found_school) == f'School({school_1.name})'


    def test_schools_save_all(
            self,
            school_repo: SchoolRepository,
            db_session: Session,
            school_1: School,
            school_2: School
    ) -> None:

        school_repo.save_all([school_1, school_2], db_session)
        db_session.flush()

        found_schools = school_repo.find_all(db_session)
        if found_schools is not None:
            assert len(found_schools) == 2
            assert found_schools[0].name == school_1.name
            assert found_schools[1].name == school_2.name


    def test_deleted_school(self, school_repo: SchoolRepository, db_session: Session, school_1: School) -> None:
        school_repo.save(school_1, db_session)
        db_session.flush()

        school_repo.delete_by_id(school_1.id, db_session)
        db_session.flush()

        deleted_school = school_repo.find_by_id(school_1.id, db_session)
        assert deleted_school is None

    def test_save_school_internal(self, school_repo_internal: SchoolRepository, school_1: School) -> None:
        school_repo_internal.save(school_1)

        found_school = school_repo_internal.find_by_name(school_1.name)
        assert found_school is not None
        assert found_school.name == school_1.name
        school_repo_internal.delete(school_1)

    def test_get_all_with_departments(self, school_repo: SchoolRepository, school_1: School,
                                      department_1: Department) -> None:
        with school_repo._get_session() as s:
            s.add_all([school_1, department_1])
            s.flush()

            schools = school_repo.get_all_with_departments(session=s)
            assert len(schools) == 1
            assert schools[0].name == school_1.name



    def test_get_session_raises_error(self) -> None:
        repo = GenericRepository[School](School, None)
        with pytest.raises(RuntimeError, match='No database session available'):
            with repo._get_session():
                pass

    def test_generic_repository_session_rollback_on_exception(self, mysql_container_engine: Engine) -> None:
        repo = GenericRepository[School](School, mysql_container_engine)
        session = Session(bind=mysql_container_engine)

        try:
            with pytest.raises(Exception):
                with repo._get_session(session=session, commit=True) as s:
                    s.execute(text('INVALID SQL SYNTAX'))
                    s.commit()
        finally:
            session.rollback()
            session.close()

    def test_generic_repository_session_rollback_internal_on_exception(self, mysql_container_engine: Engine) -> None:
        repo = GenericRepository[School](School, mysql_container_engine)
        with pytest.raises(Exception):
            with repo._get_session(session=None, commit=True) as s:
                s.execute(text('INVALID SQL SYNTAX'))
                s.commit()


class TestSchoolRepository:
    def test_get_schools_by_students_count(
            self,
            school_repo: SchoolRepository,
            db_session: Session,
            school_1: School,
            department_1: Department,
            student_1: Student) -> None:

        db_session.add_all([school_1, department_1, student_1])
        db_session.commit()

        result = school_repo.get_schools_by_students_count(db_session)

        assert result is not None
        school_result, count = result[0]
        assert school_result.name == school_1.name
        assert count == 1


    def test_get_departments_with_student_count(
            self,
            department_repo: DepartmentRepository,
            db_session: Session,
            school_1: School,
            department_1: Department,
            student_1: Student
    ) -> None:

        db_session.add_all([school_1, department_1, student_1])
        db_session.commit()

        result = department_repo.get_departments_with_student_count(db_session)
        assert result is not None
        department_result, count_student = result[0]
        assert department_result.name == department_1.name
        assert count_student == 1
        assert repr(department_result) == f'Department: {department_1.name}'

class TestStudentRepository:
    def test_get_student_by_email(self, student_repo: StudentRepository, db_session: Session, student_1: Student) -> None:
        student_repo.save(student_1, db_session)
        db_session.flush()

        result = student_repo.get_student_by_email('js@example.com', db_session)
        assert result is not None
        assert result.email == student_1.email
        assert (repr(result) ==
                f'Student: {student_1.first_name} {student_1.last_name} {student_1.gender} {student_1.age} {student_1.email}')


    def test_get_student_age_between(
            self,
            student_repo: StudentRepository,
            db_session: Session,
            student_1: Student
    ) -> None:
        student_repo.save(student_1, db_session)
        db_session.flush()
        result = student_repo.get_student_age_between(18,22,db_session)
        assert result is not None
        assert result[0].age == student_1.age

    def test_get_students_by_gender(
            self,
            student_repo: StudentRepository,
            db_session: Session,
            student_1: Student
    ) -> None:
        student_repo.save(student_1, db_session)
        db_session.flush()
        result = student_repo.get_students_by_gender(GenderEnum.MALE, db_session)
        assert result is not None
        assert result[0].gender == student_1.gender








