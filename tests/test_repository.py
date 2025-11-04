import pytest
from sqlalchemy import Engine, text
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine

from src.database.repository import SchoolRepository, StudentRepository, DepartmentRepository, GenericRepository
from src.domain.model import School, Student, Department


def test_school_save(school_repo: SchoolRepository, db_session: Session) -> None:
    school = School(name='Harvard University')
    school_repo.save(school, db_session)
    db_session.flush()

    found_school = school_repo.find_by_id(school.id, db_session)
    assert found_school is not None
    assert found_school.name == school.name
    assert repr(found_school) == f'School({school.name})'


def test_schools_save_all(school_repo: SchoolRepository, db_session: Session) -> None:
    school1 = School(name='Harvard University')
    school2 = School(name='Oxford University')
    school_repo.save_all([school1, school2], db_session)
    db_session.flush()

    found_departments = school_repo.find_all(db_session)
    if found_departments is not None:
        assert len(found_departments) == 2
        assert found_departments[0].name == school1.name
        assert found_departments[1].name == school2.name


def test_deleted_school(school_repo: SchoolRepository, db_session: Session) -> None:
    school = School(name='Harvard University')
    school_repo.save(school, db_session)
    db_session.flush()

    school_repo.delete_by_id(school.id, db_session)
    db_session.flush()

    deleted_school = school_repo.find_by_id(school.id, db_session)
    assert deleted_school is None



def test_save_school_internal(school_repo_internal: SchoolRepository) -> None:
    school = School(name='Harvard University')
    school_repo_internal.save(school)

    found_school = school_repo_internal.find_by_name(school.name)
    assert found_school.name == 'Harvard University'
    school_repo_internal.delete(school)



def test_get_all_with_departments(school_repo: SchoolRepository) -> None:
    with school_repo._get_session() as s:
        school = School(name='Harvard University')
        department = Department(name='Biology', school=school)

        s.add_all([school, department])

        schools = school_repo.get_all_with_departments(session=s)
        assert len(schools) == 1
        assert schools[0].name == 'Harvard University'


def test_get_session_raises_error() -> None:
    repo = GenericRepository[School](School, None)
    with pytest.raises(RuntimeError, match='No database session available'):
        with repo._get_session():
            pass

def test_generic_repository_session_rollback_on_exception(mysql_container_engine: Engine) -> None:
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

def test_generic_repository_session_rollback_internal_on_exception(mysql_container_engine: Engine) -> None:
    repo = GenericRepository[School](School, mysql_container_engine)
    with pytest.raises(Exception):
        with repo._get_session(session=None, commit=True) as s:
            s.execute(text('INVALID SQL SYNTAX'))
            s.commit()




