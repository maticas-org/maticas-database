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

# gets the user wrapper instance
usrs = usr_conn.users_table




def test_user_data_insertion(example_users: dict) -> None:

    results = []

    for user in example_users:
        print(f'Inserting user {example_users[user]["username"]}...')

        ans = usrs.insert_data(**example_users[user])
        results.append(ans["status"])

        print(ans)

    print('-'*50)

def test_user_auth_by_username(example_users: dict, expected_output: tuple) -> None:

    results = []

    for user in example_users:
        print(f'Authenticating user {example_users[user]["username"]}...')

        ans = usrs.auth_user_by_username(example_users[user]["username"],
                                         example_users[user]["password"])
        results.append(ans["status"])
        print(ans)

    print(tuple(results) == expected_output)
    print('-'*50)
    
def test_user_auth_by_email(example_users: dict, expected_output: tuple) -> None:

    results = []

    for user in example_users:
        print(f'Authenticating user {example_users[user]["email"]}...')

        ans = usrs.auth_user_by_email(example_users[user]["email"],
                                      example_users[user]["password"])
        results.append(ans["status"])
        print(ans)

    print(tuple(results) == expected_output)
    print('-'*50)

def test_get_user_id(example_users: dict) -> None:

    results = []

    for user in example_users:
        print(f'Getting user id for {example_users[user]["username"]}...')

        ans = usrs.get_user_id(example_users[user]["username"])
        print(ans)

    print('-'*50)


test_user_data_insertion(example_users = example_users)
test_user_auth_by_username(example_users = example_users,
                           expected_output = output_for_example_users_auth_by_username)
test_user_auth_by_email(example_users = example_users,
                           expected_output = output_for_example_users_auth_by_username)
test_get_user_id(example_users = example_users)





