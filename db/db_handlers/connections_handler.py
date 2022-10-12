from sys import path
from os.path import abspath, dirname

current_file_directory = dirname(abspath(__file__))
path.append(current_file_directory + "/define_db")
path.append(current_file_directory)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy                 import create_engine, MetaData
from dotenv                     import load_dotenv
import os

from  db_connection             import DbConnection
from  users_db_connection       import *

load_dotenv()


class ConnectionsHandler():

    def __init__(self, users_db_connection: UsrDbConnection):

        self.users_db_connection = users_db_connection
        self.start_databases()


            
    def start_databases(self) -> dict:

        """
            Starts each user's database, and stores it in a dictionary

            INPUT: 
                    None.

            OUTPUT:
                    dictionary with shape.
                    {"status": -1 o 0 , "message": "explaination"}
        """

        self.databases_and_users = self.users_db_connection.get_user_database_name_and_user_id()
        self.databases = {}

        if self.databases_and_users == None:
            return {"status": -1 , "message": "no users found"}

        for id_ in self.databases_and_users.keys():

            db = DbConnection( db_host = os.getenv("DB_HOST"),
                               db_name = self.databases_and_users[id_],
                               db_user = os.getenv("DB_USER"),
                               db_password = os.getenv("DB_PASSWORD"),
                               db_sslmode  = os.getenv("DB_SSLMODE") )

            self.databases[id_] = db
            
        return {"status": 0 , "message": "connections handler started"}



    def update_databases(self) -> dict: 

        """
            Gets the new users and for each new user starts the the connection.

            INPUT: 
                    None.

            OUTPUT:
                    Dictionary with shape.
                    {"status": -1 o 0 , "message": "explaination"}
        """

        self.databases_and_users = users_db_connection.get_user_database_name_and_user_id()

        if self.databases_and_users == None:
            return {"status": -1 , "message": "no users found"}

        previous_users_id = set(self.databases.keys())
        current_users_id  = set(self.databases_and_users.keys())

        # current_users_id - previous_users_id
        new_users = current_users_id.difference(previous_users_id)

        for new_user_id in new_users:
            self.databases[new_user_id] = DbConnection( db_host = os.getenv("DB_HOST"),
                                                        db_name = self.databases_and_users[new_user_id],
                                                        db_user = os.getenv("DB_USER"),
                                                        db_password = os.getenv("DB_PASSWORD"),
                                                        db_sslmode  = os.getenv("DB_SSLMODE") )

        return {"status": 0 , "message": "updated"}

    #------------------------------------------------------------------------#
    #                    Insert users relative data                          #
    #------------------------------------------------------------------------#

    def add_user(self, username: str, email: str, password: str) -> dict:
        return self.users_db_connection.add_user(username, email, password)


    def add_mic(self, username: str, api_key: str, mac_address: str, mic_name: str) -> dict:
        return self.users_db_connection.add_mic(username, api_key, mac_address, mic_name)


    def add_topic(self, username:str, api_key: str, topic: str) -> dict:
        return self.users_db_connection.add_topic(username, api_key, topic)

    #------------------------------------------------------------------------#
    #                   User authentication operations                       #
    #------------------------------------------------------------------------#

    def auth_user_by_username(self, username: str, password: str) -> dict:
        return self.users_db_connection.auth_user_by_username(username, password)


    def auth_user_by_email(self, email: str, password: str) -> dict:
        return self.users_db_connection.auth_user_by_email(email, password)
    
    #------------------------------------------------------------------------#
    #                       Get user data operations                         #
    #------------------------------------------------------------------------#

    def get_user_id(self, username: str) -> dict:

        ans = self.users_db_connection.get_user_id(username)
        return ans


    def get_mic_data_by_usr_and_mac(self, username: str, mac_address: str) -> dict:
        return self.users_db_connection.get_mic_data_by_usr_and_mac(username, mac_address)


    
    def read_ambient_data(self, username: str, api_key: str, varname: str, timestamp_start: str, timestamp_end: str) -> dict:

        check = self.users_db_connection.check_credentials(username, api_key)
        if check["status"] == -1:
            return check

        usr_id = self.get_user_id(username)

        if usr_id["status"] == -1:
            return usr_id

        return self.databases[usr_id["id"]].read_data(varname, timestamp_start, timestamp_end)


    def read_ambiental_variable_interval(self, username: str, api_key: str, varname: str) -> dict:

        check = self.users_db_connection.check_credentials(username, api_key)
        if check["status"] == -1:
            return check

        usr_id = self.get_user_id(username)

        if usr_id["status"] == -1:
            return usr_id

        return self.databases[usr_id["id"]].read_ambiental_variable_interval(varname)


    def read_actuators_configuration(self, username: str, api_key: str, actuator_name: str) -> dict:

        check = self.users_db_connection.check_credentials(username, api_key)
        if check["status"] == -1:
            return check

        usr_id = self.get_user_id(username)

        if usr_id["status"] == -1:
            return usr_id

        return self.databases[usr_id["id"]].read_actuators_configuration(actuator_name)

    #------------------------------------------------------------------------#
    #                       Write user data on his/her database              #
    #------------------------------------------------------------------------#
    def write_ambiental_data(self, value: float, varname: str, verbose = False) -> None:
        return self.databases[usr_id].write_data(value, varname, verbose)


    def write_ambiental_variable_interval(self,
                                          username: str,
                                          api_key: str,
                                          variable: str, 
                                          acceptable_interval: tuple,
                                          optimal_interval:    tuple, 
                                          verbose = False) -> dict:

        check = self.users_db_connection.check_credentials(username, api_key)
        if check["status"] == -1:
            return check

        usr_id = self.get_user_id(username)

        if usr_id["status"] == -1:
            return usr_id

        return self.databases[usr_id["id"]].write_ambiental_variable_interval(variable,
                                                                              acceptable_interval,
                                                                              optimal_interval,
                                                                              verbose)


    def write_actuators_configuration(self,
                                      username: str,
                                      api_key: str,
                                      actuator_name:  str,
                                      start_time:     str,
                                      end_time:       str,
                                      on_time:        int,
                                      off_time:       int,
                                      verbose = False) -> int:

        check = self.users_db_connection.check_credentials(username, api_key)
        if check["status"] == -1:
            return check

        usr_id = self.get_user_id(username)

        if usr_id["status"] == -1:
            return usr_id

        return self.databases[usr_id["id"]].write_actuators_configuration(actuator_name,
                                                                         start_time,
                                                                         end_time,
                                                                         on_time,
                                                                         off_time,
                                                                         verbose)


    #------------------------------------------------------------------------#
    #                       Operator overloads                               #
    #------------------------------------------------------------------------#

    def __getitem__(self, usr_id: int) -> DbConnection:

        try:
            return  self.databases[usr_id]

        except e: 
            return None








