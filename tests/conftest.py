from typing import Generator

from sqlalchemy.orm import Session
from testcontainers.mysql import MySqlContainer #type: ignore
import pytest
from sqlalchemy import Engine, create_engine

from src.database.config import Base
from src.database.repository import SchoolRepository, DepartmentRepository, StudentRepository


@pytest.fixture(scope='session')
def mysql_container_engine() -> Generator[Engine, None, None]:
    with MySqlContainer('mysql:latest') as mysql_container:
        mysql_container.start()
        engine = create_engine(mysql_container.get_connection_url(), echo=True)
        Base.metadata.create_all(engine)
        yield engine
        engine.dispose()


@pytest.fixture
def db_session(mysql_container_engine: Engine) -> Generator[Session, None, None]:
    session = Session(bind=mysql_container_engine)
    yield session
    session.rollback()
    session.close()

@pytest.fixture
def school_repo(db_session: Session) -> SchoolRepository:
    if not isinstance(db_session.bind, Engine):
        raise TypeError("Database engine must be an instance of MySqlContainer")
    return SchoolRepository(engine=db_session.bind)

@pytest.fixture
def school_repo_internal(mysql_container_engine: Engine) -> SchoolRepository:
    return SchoolRepository(engine=mysql_container_engine, expire_on_commit=False)

@pytest.fixture
def department_repo(db_session: Session) -> DepartmentRepository:
    if not isinstance(db_session.bind, Engine):
        raise TypeError("Database engine must be an instance of MySqlContainer")
    return DepartmentRepository(engine=db_session.bind)

@pytest.fixture
def student_repo(db_session: Session) -> StudentRepository:
    if not isinstance(db_session.bind, Engine):
        raise TypeError("Database engine must be an instance of MySqlContainer")
    return StudentRepository(engine=db_session.bind)


