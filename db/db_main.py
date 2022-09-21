from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy                 import create_engine
from dotenv                     import load_dotenv
from models                     import *
import os

load_dotenv()

Base = declarative_base()

conn_string = f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}/{os.getenv("DB_NAME")}'
print(conn_string)

engine = create_engine(conn_string)
Base.metadata.create_all(engine)



