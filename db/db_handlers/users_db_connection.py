import datetime
import pytz
import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table, Column, DateTime, Float, insert, select, delete

from sys import path
from os.path import abspath, dirname

# the directory where the database is defined to the path
root_dir = dirname(dirname(abspath(__file__)))
path.append( root_dir + "/define_db" )

# imports database tables definitions 
from tables_utilities   import *


class UsrDbConnection():

    #-----------------------------------------------#
    # Initialization and configuration of the class #
    #-----------------------------------------------#

    def __init__(self, 
                 db_host: str,
                 db_name: str,
                 db_user: str,
                 db_password: str,
                 db_sslmode: str ):

        print("Starting Users database connection...")

        self.db_host = db_host
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_sslmode = db_sslmode
        self.metadata  = MetaData()

        conn_string = f'postgresql://{self.db_user}:{self.db_password}@{self.db_host}/{self.db_name}'
        print(conn_string)

        self.engine = create_engine(conn_string)
        self.configure_connection()

        print("Done creating Users database connection.")
        print("-"*60)
            

    def configure_connection(self) -> None:

        """
        """

        tables = load_users_tables(self.engine, self.metadata)

        self.users_table  = tables['users']
        self.mics_table   = tables['microcontrollers']
        self.topics_table = tables['topics']


        print("Done starting the users database.")
        print("-"*60)


    ############################################################# 
    #-----------------------------------------------------------#
    #                                                           #
    #-----------------------------------------------------------#


    def add_user(self, username: str, email: str, password: str) -> None:

        """
        """

        result = self.users_table.insert_data(username = username,
                                              email    = email,
                                              password = password)

        return result




    def auth_user_by_username(self, username: str, password: str) -> str:

        """
        """

        result = self.users_table.auth_user_by_username(username = username,
                                                        password = password)

        return result


    def auth_user_by_email(self, username: str, password: str) -> str:

        """
        """

        return 0



