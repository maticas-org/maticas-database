from sqlalchemy import MetaData, Table, Column, DateTime, Float, String, insert, select, delete, update 
from datetime import datetime

import pandas as pd
from sqlalchemy.dialects import postgresql


"""
Table Structure:

        +-----------+-----------------------+----------------------------------------+
        |   usr_id  |   time                |               topic                    |
        +-----------+-----------------------+----------------------------------------+
        |           |                       |                                        |
        |   int     | "YYYY/MM/DD %H:%M:%S" | "/esp32/user_name/mac_address/varname" |
        +-----------+-----------------------+----------------------------------------+
"""

class TopicsWrapper():

    def __init__(self, table: Table, engine):

        self.table = table
        self.engine = engine


    def get_all_topics(self) -> pd.DataFrame:

        """
            retrieve all the topics that the user has registered.
        """

        # select statement for the table, only takes the topic column
        statement = select(self.table.c.topic)

        # compiles the statement into a PosgresSQL query string.
        statement = statement.compile(dialect = postgresql.dialect())

        # returns a dataframe with the results
        result = pd.read_sql(statement, self.engine).to_dict("list")
        return result


    def read_data_by_usr_id(self, usr_id: int) -> pd.DataFrame:

        """
            retrieve all the topics that the user has registered.
        """

        statement = select(self.table).where(self.table.c.usr_id == usr_id)

        # compiles the statement into a PosgresSQL query string.
        statement = statement.compile(dialect = postgresql.dialect())

        # returns a dataframe with the results
        result = pd.read_sql(statement, self.engine)
        return result



    def insert_data(self, usr_id: str, usr_name:str, mac_addresses: pd.DataFrame, topic: str):

        """
            Inserts a new Topic.

            Input:
                    - usr_id:       user id that owns the microcontroller.
                    - topic:        topic to be inserted.

            Output:
                    
                    returns a dictionary with the following structure:

                    {
                        "status":   0 or -1,
                        "message":  "message"
                    }
        """

        usr_id, topic = self.sanitize_input(usr_id = usr_id,
                                            topic  = topic)

        input_check = self.insert_data_watchdog(usr_id, usr_name, mac_addresses, topic)

        if  input_check["status"] == -1:
            return input_check

        
        # insert statement for the table
        insert_statement = insert(self.table).values(usr_id = usr_id,
                                                     time   = datetime.utcnow(),
                                                     topic  = topic)


        # compiles the statement into a PosgresSQL query string.
        insert_statement = insert_statement.compile(dialect = postgresql.dialect())


        with self.engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
            connection.execute(insert_statement)

        return {"status": 0, "message": "Data inserted correctly"}



    #----------------------------------------------------------------------------#
    #                             Input check                                    #
    #----------------------------------------------------------------------------#

    def sanitize_input(self, usr_id: int, topic: str) -> tuple:

        """
            Sanitizes the input data.

            Input:
                    - usr_id:       user id that owns the microcontroller.
                    - topic:        topic to be inserted.

            Output:
                    - usr_id:       sanitized user id.
                    - topic:        sanitized topic.
        """

        # sanitizes the usr_id
        usr_id = int(usr_id)

        # sanitizes the topic
        topic = str(topic).strip()

        return usr_id, topic


    def insert_data_watchdog(self, usr_id: int,
                                   usr_name: str,
                                   mac_addresses: pd.DataFrame,
                                   topic: str) -> dict:

        """
            Checks the input data for the insert_data function.

            Input:
                    - usr_id:       user id that owns the microcontroller.
                    - usr_name:     user name that owns the microcontroller.
                    - mac_addresses:    mac addresses of the microcontrollers that the user owns.
                    - topic:        topic to be inserted.

            Output:
                    
                    returns a dictionary with the following structure:

                    {
                        "status":   0 or -1,
                        "message":  "message"
                    }
        """

        # checks if the usr_id is a int
        if not isinstance(usr_id, int):
            return {"status": -1, "message": "usr_id must be a number."}

        # checks if the topic is a string
        if not isinstance(topic, str):
            return {"status": -1, "message": "topic must be a string."}

        # checks if topic exists 
        data_check = self.check_topic_uniqueness(usr_id, topic)

        if data_check["status"] == -1:
            return data_check

        data_check = self.check_topic_fields(usr_name, mac_addresses, topic)

        if data_check["status"] == -1:
            return data_check
    

        return {"status": 0, "message": "data is correct"}


    def check_topic_uniqueness(self, usr_id: int, topic: str) -> dict:

        """
            Checks if the topic is already registered in the database.

            Input:
                    - usr_id:       user id that owns the microcontroller.
                    - topic:        topic to be inserted.

            Output:
                    
                    returns a dictionary with the following structure:

                    {
                        "status":   0 or -1,
                        "message":  "message"
                    }
        """

        # select statement for the table
        statement = select(self.table).where(self.table.c.usr_id == usr_id).where(self.table.c.topic == topic)

        # compiles the statement into a PosgresSQL query string.
        statement = statement.compile(dialect = postgresql.dialect())

        # returns a dataframe with the results
        result = pd.read_sql(statement, self.engine)

        # checks if the topic is already registered
        if not result.empty:
            return {"status": -1, "message": "topic already registered."}

        return {"status": 0, "message": "topic is unique"}


    def check_topic_fields(self, user_name: str, mac_addresses: pd.DataFrame, topic: str) -> dict:

        # the topic has this structure: 
        # "/esp32/user_name/mac_address/varname" 

        # splits the topic into a list, and extracts the user_name and mac_address into 
        # separate variables
        topic_list = topic.split("/")
        user_name_from_topic   = topic_list[1]
        mac_address_from_topic = topic_list[2]

        # checks if the user_name is the same in the topic and in the database
        if user_name != user_name_from_topic:
            return {"status": -1, "message": "user_name is not correct."}

        
        # checks if the mac_address is in the mac_addresses dataframe
        if (mac_addresses["mac_address"].eq(mac_address_from_topic)).any() == True:
           return {"status": -1, "message": "mac_address is not correct."}


        return {"status": 0, "message": "data is correct"}



