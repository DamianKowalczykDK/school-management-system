from sqlalchemy.orm import Session

from src.db.config import sync_engine, Base
from src.model import School, Department, Student


def main() -> None:
    Base.metadata.create_all(sync_engine)

    school1 = School(name='Harvard University')
    school2 = School(name='Cambridge University')

    department1 = Department(name='Mathematics', school=school1, school_id=1)
    department2 = Department(name='Biology', school=school1, school_id=1)
    department3 = Department(name='Informatica', school=school2, school_id=2)
    department4 = Department(name='Chemics', school=school2, school_id=2)

    student1 = Student(
        first_name='John',
        last_name='Smith',
        gender='M',
        age=30,
        email='JS@example.com',
        department=department1,
        department_id=1,
        school_id=1
    )
    student2 = Student(
        first_name='Jon',
        last_name='Doe',
        gender='M',
        age=25,
        email='JD@example.com',
        department=department3,
        department_id=3,
        school_id=2
    )

    with Session(sync_engine) as session:
        session.add_all([school1, school2])
        session.add_all([department1, department2, department3, department4])
        session.add_all([student1, student2])
        session.commit()


if __name__ == '__main__':
    main()