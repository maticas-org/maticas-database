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



def test_authenticate_user_by_name(verbose = False):

    """Tests user authentication"""
    title("Testing user authentication by name")

    results = []
    for user in example_users_auth:

        result = usr_conn.auth_user_by_username( example_users_auth[user]["username"],
                                                 example_users_auth[user]["password"] ) 
        results.append(result["status"])
        
        if verbose:
            print(f'testing auth: {example_users_auth[user]["username"]}...')
            print(result)

    passed(results == user_auth_output)
    print("-"*80)

#--------------------------------------------------------------------------------#

def test_authenticate_user_by_email(verbose = False):

    """Tests user authentication"""
    title("Testing user authentication by email")

    results = []
    for user in example_users_auth:


        result = usr_conn.auth_user_by_email( example_users_auth[user]["email"],
                                              example_users_auth[user]["password"] ) 
        results.append(result["status"])

        if verbose:
            print(f'testing auth: {example_users_auth[user]["username"]}...')
            print(result)

    passed(results == user_auth_output)
    print("-"*80)

#--------------------------------------------------------------------------------#

def test_user_addition(verbose = False):
    
    """Tests user addition to the database"""
    title("Testing user addition to the database")

    results = []
    for user in example_users_insertion:

        result = usr_conn.add_user(**example_users_insertion[user]) 
        results.append(result["status"])

        if verbose:
            print(f'testing auth: {example_users_insertion[user]["username"]}...')
            print(result)

    passed(results == user_insertion_output)
    print("-"*80)

#--------------------------------------------------------------------------------#

def test_mic_adittion(verbose = False):

    """Tests user addition to the database"""
    title("Testing user mic addition to the database")

    results = []
    for user in example_mics_insertion:

        result = usr_conn.add_mic(**example_mics_insertion[user])
        results.append(result["status"])

        if verbose:
            print(f'testing auth: {example_mics_insertion[user]["username"]}...')
            print(result)

    passed(results == mics_insertion_output)
    print("-"*80)

#--------------------------------------------------------------------------------#

def test_topic_adittion(verbose = False):

    """Tests user addition to the database"""
    title("Testing user topic addition to the database")

    results = []
    for user in example_topics_insertion:

        result = usr_conn.add_topic(**example_topics_insertion[user])
        results.append(result["status"])

        if verbose:
            print(f'testing auth: {example_topics_insertion[user]["username"]}...')
            print(result)

    passed(results == topics_insertion_output)
    print("-"*80)


# at first time run this test is passed because the database is empty
# but after the first run, the database is not empty anymore, this fact will be called [1]
test_user_addition(verbose = False)

test_authenticate_user_by_name(verbose = False)
test_authenticate_user_by_email(verbose = False)
test_mic_adittion(verbose = False)

# also has issue [1]
test_topic_adittion(verbose = False)



