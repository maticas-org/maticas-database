from sys import path
from os.path import abspath, dirname

current_file_directory = dirname(abspath(__file__))
path.append(current_file_directory + "/define_db")

from tables_utilities import load_all_tables

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy                 import create_engine, MetaData
from dotenv                     import load_dotenv
import os

load_dotenv()
metadata_obj = MetaData()

conn_string = f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}/{os.getenv("DB_NAME")}'
print(conn_string)

engine = create_engine(conn_string)
tables = load_all_tables(engine = engine, metadata = metadata_obj)
print(tables)



