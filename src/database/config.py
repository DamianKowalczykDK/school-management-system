from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

USER=os.getenv('DB_USER')
PASSWORD=os.getenv('DB_PASSWORD')
HOST=os.getenv('DB_HOST')
PORT=os.getenv('DB_PORT')
DATABASE=os.getenv('DB_DATABASE')
URL=f'mysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'

sync_engine = create_engine(URL, echo=True)

class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models.

     This class is used as the declarative base for all ORM model
     definitions in the application. Any model inheriting from this
     base will automatically be registered with SQLAlchemy’s metadata.

     Example:
         class Student(Base):
             __tablename__ = "students"
             id = mapped_column(Integer, primary_key=True)

     Attributes:
         metadata (MetaData): Contains the database schema and object mappings.
     """
    pass


