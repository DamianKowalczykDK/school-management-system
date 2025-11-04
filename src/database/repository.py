from sqlalchemy import Engine, select, func
from sqlalchemy.orm import Session, joinedload
from contextlib import contextmanager
from src.database.config import Base
from typing import Type, Generator
from src.database.config import logger
from src.domain.model import School, Department, Student, GenderEnum


class GenericRepository[T: Base]:
    def __init__(self, model_type: Type[T], engine: Engine | None = None, expire_on_commit: bool = True) -> None:
        self.model_type = model_type
        self.engine = engine
        self.expire_on_commit = expire_on_commit

    def save(self, instance: T, session: Session | None = None) -> None:
        with self._get_session(session, commit=True) as s:
            s.add(instance)

    def save_all(self, instances: list[T], session: Session | None = None) -> None:
        with self._get_session(session, commit=True) as s:
            s.add_all(instances)

    def find_by_id(self, instance_id: int, session: Session | None = None) -> T | None:
        with self._get_session(session, commit=True) as s:
            return s.get(self.model_type, instance_id)

    def find_all(self, session: Session | None = None) -> list[T] | None:
        with self._get_session(session) as s:
            stmt = select(self.model_type)
            return list(s.scalars(stmt).all())

    def delete(self, instance: T, session: Session | None = None) -> None:
        with self._get_session(session, commit=True) as s:
            s.delete(instance)

    def delete_by_id(self, instance_id: int, session: Session | None = None) -> None:
        with self._get_session(session, commit=True) as s:
            instance = self.find_by_id(instance_id, s)
            if instance:
                self.delete(instance, s)

    @contextmanager
    def _get_session(self, session: Session | None = None, commit: bool = False) -> Generator[Session, None, None]:
        managed_externally = session is not None

        if not session:
            if not self.engine:
                raise RuntimeError('No database session available')
            session = Session(self.engine, expire_on_commit=self.expire_on_commit)

        try:
            yield session
            if commit and not managed_externally:
                session.commit()
        except Exception as e:
            logger.error(e)
            if commit and not managed_externally:
                session.rollback()
            raise
        finally:
            if not managed_externally:
                session.close()

class SchoolRepository(GenericRepository[School]):
    def __init__(self, engine: Engine | None = None, expire_on_commit: bool = True) -> None:
        super().__init__(School, engine, expire_on_commit)

    def find_by_name(self, name: str, session: Session | None = None) -> School | None:
        with self._get_session(session, commit=True) as s:
            stmt = select(School).where(School.name == name)
            return s.scalar(stmt)

    def get_schools_by_students_count(self, session: Session | None = None) -> list[tuple[School, int]]:
        with self._get_session(session, commit=True) as s:
            stmt = (
                select(School, func.count(Student.id).label('count_student'))
                .outerjoin(School.departments)
                .outerjoin(Department.students)
                .group_by(School.id)
                .order_by(func.count(Student.id).desc())
            )
            result = s.execute(stmt).all()
            return [(school, count) for school, count in result]

    def get_all_with_departments(self, session: Session | None = None) -> list[School]:
        with self._get_session(session, commit=True) as s:
            stmt = select(School).options(joinedload(School.departments))
            return list(s.scalars(stmt).unique().all())

class DepartmentRepository(GenericRepository[Department]):
    def __init__(self, engine: Engine | None = None, expire_on_commit: bool = True) -> None:
        super().__init__(Department, engine, expire_on_commit)

    def get_departments_with_student_count(self, session: Session | None = None) -> list[tuple[Department, int]]:
        with self._get_session(session) as s:
            stmt = (
                select(Department, func.count(Student.id).label('count_student'))
                .outerjoin(Department.students)
                .group_by(Department.id)
                .order_by(func.count(Student.id).desc())
            )
            result = s.execute(stmt).all()
            return [(dep, count) for dep, count in result]


class StudentRepository(GenericRepository[Student]):
    def __init__(self, engine: Engine | None = None, expire_on_commit: bool = True) -> None:
        super().__init__(Student, engine, expire_on_commit)

    def get_student_by_email(self, email: str, session: Session | None = None) -> Student | None:
        with self._get_session(session, commit=True) as s:
            stmt = select(Student).where(Student.email == email)
            student = s.scalar(stmt)
            if student is None:
                raise ValueError('Student not found')
            return student


    def get_student_age_between(self, min_age: int, max_age:int, session: Session | None = None) -> list[Student]:
        with self._get_session(session, commit=True) as s:
            stmt = select(Student).where(Student.age.between(min_age, max_age))
            return list(s.scalars(stmt).all())

    def get_students_by_gender(self, gender: GenderEnum, session: Session | None = None) -> list[Student]:
        with self._get_session(session, commit=True) as s:
            stmt = select(Student).where(Student.gender == gender)
            return list(s.scalars(stmt).all())
