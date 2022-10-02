from sqlalchemy import MetaData, Table, Column, DateTime, Float, String, insert, select, delete, update 
from datetime import datetime

import pandas as pd
from sqlalchemy.dialects import postgresql


"""
    Microcontrollers table, this table contains the microcontrollers that the user has registered.


    Table Structure:

        +-----------+-----------------------+------------------------+----------------------+
        |   usr_id  |   time                |        name            |      mac_address     |
        +-----------+-----------------------+------------------------+----------------------+
        |           |                       |                        |                      |
        |   int     | "YYYY/MM/DD %H:%M:%S" | "microcontroller name" |  "xx:yy:cc:ww:ee:dd" |
        +-----------+-----------------------+------------------------+----------------------+
"""


class MicrocontrollersWrapper():

    def __init__(self, table: Table, engine):

        self.table = table
        self.engine = engine


    def read_data_by_usr_id(self, usr_id: str) -> pd.DataFrame:

        """
            returns the user microcontroller mac addresses.
        """

        statement = select(self.table.c.mac_address).where(self.table.c.usr_id == usr_id)

        # compiles the statement into a PosgresSQL query string.
        statement = statement.compile(dialect = postgresql.dialect())

        # returns a dataframe with the results
        result = pd.read_sql(statement, self.engine)
        return result


    def read_data_by_usr_id_and_mac(self, usr_id: str, mac_address: str) -> pd.DataFrame:

        """
            Reads of the selected actuator.
        """

        statement = select(self.table).where(self.table.c.usr_id == usr_id).\
                                       where(self.table.c.mac_address == mac_address)

        # compiles the statement into a PosgresSQL query string.
        statement = statement.compile(dialect = postgresql.dialect())

        # returns a dataframe with the results
        result = pd.read_sql(statement, self.engine)
        return result


    def insert_data(self, usr_id: str, name: str, mac_address: str):

        """
            Inserts a new microcontroller.

            Input:
                    - usr_id:       user id that owns the microcontroller.
                    - name:         microcontroller name.
                    - mac_address:  microcontroller mac address.

            Output:
                    
                    returns a dictionary with the following structure:

                    {
                        "status":   0 or -1,
                        "message":  "message"
                    }
        """

        usr_id, name, mac_address = self.sanitize_input(usr_id = usr_id,
                                                        mic_name = name,
                                                        mac_address = mac_address)

        input_check = self.insert_data_watchdog(usr_id, name, mac_address)

        if  input_check["status"] == -1:
            return input_check

        
        # insert statement for the table
        insert_statement = insert(self.table).values(usr_id = usr_id,
                                                     time = datetime.utcnow(),
                                                     name   = name,
                                                     mac_address = mac_address)

        # statement for deletion of previous data
        delete_statement = delete(self.table).where(self.table.c.name == name).\
                                              where(self.table.c.usr_id == usr_id)

        # compiles the statement into a PosgresSQL query string.
        insert_statement = insert_statement.compile(dialect = postgresql.dialect())
        delete_statement = delete_statement.compile(dialect = postgresql.dialect())


        with self.engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
            connection.execute(delete_statement)
            connection.execute(insert_statement)

        return {"status": 0, "message": "Data inserted correctly"}

    #---------------------------------------------------------------#
    #                   data check functions                        #
    #---------------------------------------------------------------#


    def insert_data_watchdog(self, usr_id: int, name: str, mac_address: str) -> dict:

        """
            Checks the input data for the insert_data function.

            Input:
                    - usr_id:       user id that owns the microcontroller.
                    - name:         microcontroller name.
                    - mac_address:  microcontroller mac address.

            Output:
                    
                    returns a dictionary with the following structure:

                    {
                        "status":   0 or -1,
                        "message":  "message"
                    }
        """

        # checks if the usr_id is a string
        if not isinstance(usr_id, int):
            return {"status": -1, "message": "usr_id must be a number"}

        # checks if the name is a string
        if not isinstance(name, str):
            return {"status": -1, "message": "name must be a string"}

        # checks if the mac_address is a string
        if not isinstance(mac_address, str):
            return {"status": -1, "message": "mac_address must be a string"}

        return {"status": 0, "message": "Data is correct"}


    #---------------------------------------------------------------#
    #               data sanitization functions                     #
    #---------------------------------------------------------------#

    def sanitize_input(self, usr_id: int, mic_name: str, mac_address: str):
        return self.sanitize_usr_id(usr_id),  self.sanitize_name(mic_name), self.sanitize_mac(mac_address)


    def sanitize_usr_id(self, usr_id: int):
        return usr_id

    def sanitize_mac(self, mac_address: str):
        return mac_address.strip()

    def sanitize_name(self, mic_name: str):
        return mic_name.strip()






