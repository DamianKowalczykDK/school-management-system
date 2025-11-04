from src.database.config import sync_engine, Base
from src.database.repository import SchoolRepository, StudentRepository, DepartmentRepository
from src.domain.model import School, Department, Student, GenderEnum
from src.service.school_management_service import SchoolManagementService


def main() -> None:
    Base.metadata.create_all(sync_engine)

    school1 = School(name='Harvard University')
    school2 = School(name='Cambridge University')

    department1 = Department(name='Mathematics', school=school1, school_id=1)
    department2 = Department(name='Biology', school=school1, school_id=1)
    department3 = Department(name='Informatica', school=school2, school_id=2)
    department4 = Department(name='Chemistry', school=school2, school_id=2)

    student1 = Student(
        first_name='John',
        last_name='Smith',
        gender=GenderEnum.MALE,
        age=30,
        email='JS@example.com',
        department=department1,
        department_id=1,
    )
    student2 = Student(
        first_name='Jon',
        last_name='Doe',
        gender=GenderEnum.MALE,
        age=25,
        email='JD@example.com',
        department=department3,
        department_id=3,
    )

    # school_repo = SchoolRepository(engine=sync_engine)
    # school_repo.save_all([school1, school2])
    #
    # with Session(sync_engine) as s:
    #     department_repo = DepartmentRepository(engine=sync_engine)
    #     # department_repo.save_all([department1, department2, department3, department4])
    #     dep = department_repo.popular_department(session=s)
    #     for d in dep:
    #         print(d)

    # students_repo = StudentRepository(engine=sync_engine)
    # students_repo.save_all([student1, student2])

    student_repo = StudentRepository(engine=sync_engine, expire_on_commit=False)
    # stud = student_repo.find_student_by_email('JS@example.com')
    # print(stud)
    # students = student_repo.find_student_age_between(21,31)
    # for stud in students:
    #     print(stud)

    # department_repo = DepartmentRepository(engine=sync_engine, expire_on_commit=False)
    # dep = department_repo.get_department()
    # if dep is not None:
    #     for d in dep:
    #         print(f'{d}')

    # school = school_repo.get_most_students()
    # for student in school:
    #     print(student)
    # schools = school_repo.get_all_with_departments()
    # for school in schools:
    #     print(f'School: {school.name}, {school.departments}')


    student_repo = StudentRepository(engine=sync_engine, expire_on_commit=False)
    department_repo = DepartmentRepository(engine=sync_engine, expire_on_commit=False)
    school_repo = SchoolRepository(engine=sync_engine, expire_on_commit=False)

    school_management_service = SchoolManagementService(school_repo=school_repo, student_repo=student_repo, department_repo=department_repo)
    # print(school_management_service.most_popular_department())
    # print(school_management_service.students_by_gender(gender=GenderEnum.MALE))
    # print(school_management_service.school_with_all_departments())
    # print(school_management_service.find_student_between_age_range(26, 40))
    print(school_management_service.find_student_by_email("JS@example.com"))








if __name__ == '__main__':
    main()