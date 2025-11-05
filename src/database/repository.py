from src.domain.model import School, Department, Student, GenderEnum
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import Engine, select, func
from src.database.config import logger
from contextlib import contextmanager
from src.database.config import Base
from typing import Type, Generator


class GenericRepository[T: Base]:
    """Generic repository providing common CRUD operations for SQLAlchemy models.

    This class acts as a base repository for other specific repositories.
    It handles session management, saving, retrieving, and deleting entities.

    Attributes:
        model_type (Type[T]): SQLAlchemy model class used by this repository.
        engine (Engine | None): Optional SQLAlchemy engine used for creating sessions.
        expire_on_commit (bool): Whether to expire objects on commit (default: True).
    """

    def __init__(self, model_type: Type[T], engine: Engine | None = None, expire_on_commit: bool = True) -> None:
        """Initializes the generic repository.

        Args:
            model_type (Type[T]): SQLAlchemy model class.
            engine (Engine | None): Optional database engine.
            expire_on_commit (bool): Whether to expire objects on commit.
        """
        self.model_type = model_type
        self.engine = engine
        self.expire_on_commit = expire_on_commit

    def save(self, instance: T, session: Session | None = None) -> None:
        """Saves a single model instance.

        Args:
            instance (T): The model instance to save.
            session (Session | None): Optional SQLAlchemy session.
        """
        with self._get_session(session, commit=True) as s:
            s.add(instance)

    def save_all(self, instances: list[T], session: Session | None = None) -> None:
        """Saves multiple model instances at once.

        Args:
            instances (list[T]): List of model instances to save.
            session (Session | None): Optional SQLAlchemy session.
        """
        with self._get_session(session, commit=True) as s:
            s.add_all(instances)

    def find_by_id(self, instance_id: int, session: Session | None = None) -> T | None:
        """Finds an entity by its primary key ID.

        Args:
            instance_id (int): The entity ID.
            session (Session | None): Optional SQLAlchemy session.

        Returns:
            T | None: Found entity instance or None if not found.
        """
        with self._get_session(session, commit=True) as s:
            return s.get(self.model_type, instance_id)

    def find_all(self, session: Session | None = None) -> list[T] | None:
        """Finds all entities for the given model.

        Args:
            session (Session | None): Optional SQLAlchemy session.

        Returns:
            list[T] | None: List of all found entities.
        """
        with self._get_session(session) as s:
            stmt = select(self.model_type)
            return list(s.scalars(stmt).all())

    def delete(self, instance: T, session: Session | None = None) -> None:
        """Deletes a specific entity instance.

        Args:
            instance (T): The model instance to delete.
            session (Session | None): Optional SQLAlchemy session.
        """
        with self._get_session(session, commit=True) as s:
            s.delete(instance)

    def delete_by_id(self, instance_id: int, session: Session | None = None) -> None:
        """Deletes an entity by its ID.

        Args:
            instance_id (int): ID of the entity to delete.
            session (Session | None): Optional SQLAlchemy session.
        """
        with self._get_session(session, commit=True) as s:
            instance = self.find_by_id(instance_id, s)
            if instance:
                self.delete(instance, s)

    @contextmanager
    def _get_session(self, session: Session | None = None, commit: bool = False) -> Generator[Session, None, None]:
        """Provides a managed SQLAlchemy session context.

        If no session is passed, a new one will be created using the configured engine.

        Args:
            session (Session | None): Existing SQLAlchemy session or None to create a new one.
            commit (bool): Whether to commit at the end of the context.

        Yields:
            Session: Active SQLAlchemy session.

        Raises:
            RuntimeError: If no session or engine is available.
        """
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
    """Repository for managing `School` entities."""

    def __init__(self, engine: Engine | None = None, expire_on_commit: bool = True) -> None:
        """Initializes the repository for `School` entities."""
        super().__init__(School, engine, expire_on_commit)

    def find_by_name(self, name: str, session: Session | None = None) -> School | None:
        """Finds a school by its name.

        Args:
            name (str): School name.
            session (Session | None): Optional SQLAlchemy session.

        Returns:
            School | None: Found school or None.
        """
        with self._get_session(session, commit=True) as s:
            stmt = select(School).where(School.name == name)
            return s.scalar(stmt)

    def get_schools_by_students_count(self, session: Session | None = None) -> list[tuple[School, int]]:
        """Retrieves schools along with their student counts.

        Args:
            session (Session | None): Optional SQLAlchemy session.

        Returns:
            list[tuple[School, int]]: List of tuples (School, student_count), sorted descending.
        """
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
        """Retrieves all schools with their departments eagerly loaded.

        Args:
            session (Session | None): Optional SQLAlchemy session.

        Returns:
            list[School]: List of schools with departments.
        """
        with self._get_session(session, commit=True) as s:
            stmt = select(School).options(joinedload(School.departments))
            return list(s.scalars(stmt).unique().all())


class DepartmentRepository(GenericRepository[Department]):
    """Repository for managing `Department` entities."""

    def __init__(self, engine: Engine | None = None, expire_on_commit: bool = True) -> None:
        """Initializes the repository for `Department` entities."""
        super().__init__(Department, engine, expire_on_commit)

    def get_departments_with_student_count(self, session: Session | None = None) -> list[tuple[Department, int]]:
        """Retrieves departments along with the number of students in each.

        Args:
            session (Session | None): Optional SQLAlchemy session.

        Returns:
            list[tuple[Department, int]]: List of (Department, student_count) tuples.
        """
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
    """Repository for managing `Student` entities."""

    def __init__(self, engine: Engine | None = None, expire_on_commit: bool = True) -> None:
        """Initializes the repository for `Student` entities."""
        super().__init__(Student, engine, expire_on_commit)

    def get_student_by_email(self, email: str, session: Session | None = None) -> Student | None:
        """Finds a student by email address.

        Args:
            email (str): Student's email.
            session (Session | None): Optional SQLAlchemy session.

        Returns:
            Student | None: Found student.

        Raises:
            ValueError: If no student is found.
        """
        with self._get_session(session, commit=True) as s:
            stmt = select(Student).where(Student.email == email)
            student = s.scalar(stmt)
            if student is None:
                raise ValueError('Student not found')
            return student

    def get_student_age_between(self, min_age: int, max_age: int, session: Session | None = None) -> list[Student]:
        """Finds all students whose ages fall within a given range.

        Args:
            min_age (int): Minimum age.
            max_age (int): Maximum age.
            session (Session | None): Optional SQLAlchemy session.

        Returns:
            list[Student]: List of matching students.
        """
        with self._get_session(session, commit=True) as s:
            stmt = select(Student).where(Student.age.between(min_age, max_age))
            return list(s.scalars(stmt).all())

    def get_students_by_gender(self, gender: GenderEnum, session: Session | None = None) -> list[Student]:
        """Finds all students of a given gender.

        Args:
            gender (GenderEnum): Gender enum value.
            session (Session | None): Optional SQLAlchemy session.

        Returns:
            list[Student]: List of matching students.
        """
        with self._get_session(session, commit=True) as s:
            stmt = select(Student).where(Student.gender == gender)
            return list(s.scalars(stmt).all())
