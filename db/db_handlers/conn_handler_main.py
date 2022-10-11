from  users_db_connection   import *
from  connections_handler   import *
from dotenv import load_dotenv
import os
load_dotenv()

usr_conn = UsrDbConnection( db_host =  os.getenv("USR_DB_HOST"),
                            db_name =  os.getenv("USR_DB_NAME"),
                            db_user =  os.getenv("USR_DB_USER"),
                            db_password = os.getenv("USR_DB_PASSWORD"),
                            db_sslmode  = os.getenv("USR_DB_SSLMODE") )



conn_handler = ConnectionsHandler(usr_conn)

