from sys import path
from os.path import abspath, dirname

# the directory where the database is defined to the path
root_dir = dirname(dirname(abspath(__file__)))
path.append(root_dir)


from db_handlers.users_db_connection import *
from test_data_definition import *

from dotenv import load_dotenv
import os

load_dotenv()

# creates a user database connection
usr_conn = UsrDbConnection( db_host =  os.getenv("USR_DB_HOST"),
                            db_name =  os.getenv("USR_DB_NAME"),
                            db_user =  os.getenv("USR_DB_USER"),
                            db_password = os.getenv("USR_DB_PASSWORD"),
                            db_sslmode  = os.getenv("USR_DB_SSLMODE") )

# gets the microcontroller wrapper instance
mics = usr_conn.mics_table


