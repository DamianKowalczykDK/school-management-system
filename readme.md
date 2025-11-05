# 🎓 School Management System

A Python-based system for managing schools, departments, and students using a clean architecture.
It integrates MySQL for persistent data storage, SQLAlchemy ORM for database interaction, Poetry for dependency management, and Pytest for testing.
The system is modular and scalable, designed with clear separation between domain, repository, service, and DTO layers.

## 🧱 Project Structure
```
src/
├── database/
│   ├── config.py
│   └── repository.py
├── domain/
│   └── model.py
├── service/
│   ├── dto.py
│   └── school_management_service.py
tests/
├── test_database/
└── test_service/
```
## ⚙️ Requirements

- Python 3.13.2
- MySQL (running instance)
- Alembic (for database migrations)
- Poetry (for dependency management)
- Docker & Docker Compose 

## 🚀 Installation & Setup
1️⃣ Clone the repository
```bash
git clone https://github.com/DamianKowalczykDK/school-management-system.git
```

2️⃣ Create a virtual environment & install dependencies
```bash
poetry install
poetry shell
```
3️⃣ Configure environment variables

Create a .env file in the project root with the following content:
```bash
DB_HOST=localhost
DB_PORT=3307
DB_DATABASE=school_db
DB_USER=your_login
DB_PASSWORD=your_password
```

## 🐳 Docker Setup

The project supports Docker Compose for simplified setup of both the application and MySQL database.

1️⃣ Start the services
```bash
docker-compose up -d --build
```
2️⃣ Stop the services
```bash
docker-compose down
```

## 🔧 Database Migrations (Alembic)
This project uses Alembic to manage and version database schema changes.

1️⃣ Initialize Alembic (only once)
```bash
- alembic init migrations
```
This creates a migrations/ folder containing Alembic’s configuration files.

2️⃣ Configure Alembic

In the alembic.ini file, update the database URL:
```bash
sqlalchemy.url = mysql://<DB_USER>:<DB_PASSWORD>@<DB_HOST>:<DB_PORT>/<DB_NAME> 
```
- copy your URL from config.py

3️⃣ Generate a new migration
```bash
alembic revision --autogenerate -m "create initial tables"
```
4️⃣ Apply migrations
```bash
alembic upgrade head
```
5️⃣ Downgrade (if needed)
```bash
alembic downgrade -1
```
## 🧩 Features

The system provides a layered architecture for efficient and maintainable management of school data.

Core functionalities:

🎓 School Management

- Add, retrieve, update, and delete schools using the GenericRepository base methods
- Fetch schools along with their departments via get_all_with_departments()

🏛️ Department Management

- Manage departments assigned to schools
- Retrieve departments with student count statistics

👩‍🎓 Student Management

- Register and manage student data
- Filter students by gender
- Search students by email
- Retrieve students within a specific age range

📊 Analytical & Reporting Functions

- Most popular departments by student count

Students filtered and transformed into DTO objects for presentation

## 🧠 Architecture Layers
Layer	Description
domain	Contains ORM models (School, Department, Student, GenderEnum)
database	Handles database configuration and repository logic
service	Business logic orchestrated through service classes
dto	Data transfer objects between repository and service layers
## 🧪 Tests & Coverage

Run all tests with coverage using:
```bash
poetry run pytest --cov=src --cov-report=html
```
- View HTML coverage report online: https://damiankowalczykdk.github.io/school-management-system/

✅ Test coverage: 100% (target)
## 🧰 Tech Stack
| Category                        | Technology / Library              | Description                                               |
| ------------------------------- | --------------------------------- | --------------------------------------------------------- |
| **Language**                    | 🐍 Python 3.13                    | Core programming language                                 |
| **ORM / Database Layer**        | 🧩 SQLAlchemy                     | Object-relational mapping and session management          |
|                                 | 🏗️ Alembic                       | Database migrations and schema versioning                 |
| **Database**                    | 🗄️ MySQL                         | Persistent relational data storage                        |
| **Dependency Management**       | 📦 Poetry                         | Handles project dependencies and virtual environment      |
| **Environment Management**      | 🌱 Python-dotenv                  | Loads environment variables from `.env`                   |
| **Logging**                     | 🧾 Python Logging                 | Configured via `src.database.config` for system-wide logs |
| **Testing Framework**           | 🧪 Pytest                         | Unit and integration testing framework                    |
| **Static Type Checking**        | 🧠 mypy                           | Ensures type safety across the codebase                   |
| **Type Hints**                  | ✍️ Typing + SQLAlchemy 2.0 Mapped | Static type definitions and ORM field mappings            |
| **Containerization (optional)** | 🐳 Docker & Docker Compose        | For running the app and MySQL in isolated environments    |
## 🧭 Planned Features
- REST API layer using FastAPI or Flask for managing schools, departments, and students
- Integration tests for API endpoints
- Extension of existing Docker setup to include the API service
- CI/CD automation for testing and deployment
## 👤 Author
- Created by Damian Kowalczyk
## 📝 License
- MIT License.