from sys    import path
from os.path import abspath, dirname

root_dir = dirname(dirname(abspath(__file__)))
path.append(root_dir)

from tables_utilities import load_all_tables
from dotenv import load_dotenv
import os

load_dotenv()


conn = DbConnection( db_host = os.getenv("DB_HOST"),
                     db_name = os.getenv("USRS_DB_NAME"),
                     db_user = os.getenv("DB_USER"),
                     db_password = os.getenv("DB_PASSWORD"),
                     db_sslmode  = os.getenv("DB_SSLMODE") )

