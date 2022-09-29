from sys import path
from os.path import abspath, dirname

current_file_directory = dirname(abspath(__file__))
path.append(current_file_directory + "/define_db")

from tables_utilities import load_all_tables

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy                 import create_engine, MetaData
from  db_connection             import DbConnection
from dotenv                     import load_dotenv
import os

load_dotenv()
metadata_obj = MetaData()


conn = DbConnection( db_host = os.getenv("DB_HOST"),
                     db_name = os.getenv("DB_NAME"),
                     db_user = os.getenv("DB_USER"),
                     db_password = os.getenv("DB_PASSWORD"),
                     db_sslmode  = os.getenv("DB_SSLMODE") )

