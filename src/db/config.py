from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
load_dotenv()

USER=os.getenv('DB_USER')
PASSWORD=os.getenv('DB_PASSWORD')
HOST=os.getenv('DB_HOST')
PORT=os.getenv('DB_PORT')
DATABASE=os.getenv('DB_DATABASE')
URL=f'mysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'

sync_engine = create_engine(URL, echo=True)

class Base(DeclarativeBase):
    pass


