from sys import path
from os.path import abspath, dirname

# the directory where the database is defined to the path
root_dir = dirname(dirname(abspath(__file__)))
path.append(root_dir)


from db_handlers.users_db_connection import *
from dotenv import load_dotenv
import os

load_dotenv()

usr_conn = UsrDbConnection( db_host =  os.getenv("USR_DB_HOST"),
                            db_name =  os.getenv("USR_DB_NAME"),
                            db_user =  os.getenv("USR_DB_USER"),
                            db_password = os.getenv("USR_DB_PASSWORD"),
                            db_sslmode  = os.getenv("USR_DB_SSLMODE") )

usrs = usr_conn.users_table

# example users to be added to the database
# for testing input validation and database insertion
example_users = {
                    "user1": {"username":   "user1",
                              "email":      "email@email.com", 
                              "password":   "ultrasecurepassword"},
                    "user2": {"username":   "user2",
                              "email":      "email@gmail.com",
                              "password":   "ultrasecurepassword123"},
                    "user22": {"username":   "user2 ",
                              "email":      "email@gmail.com",
                              "password":   "ultrasecurepassword"},

                    "user3": {"username":   "user3",
                              "email":      "imnotanemail",
                              "password":   "ultrasecurepassword"},

                    "user4": {"username":   "user4",
                              "email":      "anotheremail@",
                              "password":   "ultrasecurepassword"},
                }

output = (0, 0, -1, -1, -1)



def test_user_data_insertion(example_users: dict, desired_output: tuple) -> None:

    results = []

    for user in example_users:
        print(f'Inserting user {user}...')

        ans = usrs.insert_data(**example_users[user])
        results.append(ans["status"])

        print(ans)

    assert tuple(results) == desired_output


test_user_data_insertion(example_users, output)
