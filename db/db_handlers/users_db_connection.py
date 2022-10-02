import datetime
import pytz
import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table, Column, DateTime, Float, insert, select, delete
from sqlalchemy_utils import database_exists, create_database

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

        # create a database (if it doesn't exist)
        if not database_exists(self.engine.url):
            create_database(self.engine.url)
            print('Database created!')

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



    #------------------------------------------------------------------------#
    #                           Insert operations                            #
    #------------------------------------------------------------------------#

    def add_user(self, username: str, email: str, password: str) -> dict:

        """
        """

        result = self.users_table.insert_data(username = username,
                                              email    = email,
                                              password = password)

        return result


    def add_mic(self, username: str, api_key: str, mac_address: str, mic_name: str) -> dict:

        """
        """

        user_info = self.check_credentials(username = username, api_key = api_key)

        if user_info["status"] == -1:
            return user_info

        result = self.mics_table.insert_data(usr_id = int(user_info["user_id"]),
                                             mac_address = mac_address,
                                             name = mic_name)
        return result


    def add_topic(self, username:str, api_key: str, topic: str) -> dict:


        user_info = self.check_credentials(username = username, api_key = api_key)

        if user_info["status"] == -1:
            return user_info

        # gets the dataframes of the mac adresses the user has registered
        mac_addresses = self.mics_table.read_data_by_usr_id(int(user_info["user_id"]))

        result = self.topics_table.insert_data(usr_id    = int(user_info["user_id"]),
                                               usr_name  = username,
                                               mac_addresses = mac_addresses,
                                               topic     = topic)

        return result


    #------------------------------------------------------------------------#
    #                   Authentication operations                            #
    #------------------------------------------------------------------------#

    def auth_user_by_username(self, username: str, password: str) -> dict:

        """
        """

        result = self.users_table.auth_user_by_username(username = username,
                                                        password = password)

        return result


    def auth_user_by_email(self, email: str, password: str) -> dict:

        """
        """

        result = self.users_table.auth_user_by_email(email = email,
                                                     password = password)

        return result


    #------------------------------------------------------------------------#
    #                             Read operations                            #
    #------------------------------------------------------------------------#


    def get_mic_data_by_usr_and_mac(self, username: str, mac_address: str) -> dict:

        """
        """

        # query the user id
        user_id = self.users_table.get_user_id(username = username)

        # if the user id is not found, return the result from the query
        if user_id["status"] == -1:
            return user_id

        # if found, query the microcontroller data
        result = self.mics_table.get_mic_data_by_usr_and_mac(usr_id = int(usr_id["message"]),
                                                             mac_address = mac_address)

        return result

    #------------------------------------------------------------------------#
    #                             Check credentials                          #
    #------------------------------------------------------------------------#

    def check_credentials(self, username: str, api_key: str) -> dict:

        """
        """

        # query the user id and api key
        user_info = self.users_table.get_user_id_and_api_key(username = username)

        # checks if input data is correct
        if user_info["status"] == -1:
            return user_info

        if api_key != user_info["api_key"]:
            return {"status": -1, "message": "Invalid API key."}

        return user_info

