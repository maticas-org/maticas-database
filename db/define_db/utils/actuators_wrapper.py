from sqlalchemy import MetaData, Table, Column, DateTime, Float, String, insert, select, delete, update 
from datetime import datetime

import pandas as pd
from sqlalchemy.dialects import postgresql

"""
    This module is a wrapper for the actuators table.
    It contains all the functions that are needed to interact with the actuators table.

    The table structure is the following:

    +-----------------------+-----------------+----------------+---------------+--------------+------------------+
    |   time                |   actuator      |   start_time   |   end_time    |   time_on    |   time_off       |
    |-----------------------+-----------------+----------------+---------------+--------------+------------------+
    |                       |                 |                |               |              |                  |
    | "YYYY/MM/DD %H:%M:%S" | "actuator_name" |   "%H:%M:%S"   |  "%H:%M:%S"   |    nminutos  |     nminutos     |
    +-----------------------+-----------------+----------------+---------------+--------------+------------------+
"""

class ActuatorsWrapper():

    def __init__(self, table: Table, engine):

        self.table = table
        self.engine = engine


    def read_all_data(self) -> pd.DataFrame:

        """
            Reads all the data from the actuators table.
        """

        statement = select(self.table)

        # compiles the statement into a PosgresSQL query string.
        statement = statement.compile(dialect = postgresql.dialect())

        # returns a dataframe with the results
        result = pd.read_sql(statement, self.engine)
        return result


    def read_data(self, actuator: str) -> pd.DataFrame:

        """
            Reads of the selected actuator.
        """

        statement = select(self.table).where(self.table.c.actuator_name == actuator)

        # compiles the statement into a PosgresSQL query string.
        statement = statement.compile(dialect = postgresql.dialect())

        # returns a dataframe with the results
        result = pd.read_sql(statement, self.engine)
        return result


    def insert_data(self, actuator:     str,
                          start_time:   str,
                          end_time:     str, 
                          time_on:      int,
                          time_off:     int) -> dict:

        """
            Inserts data into the actuators table.

            Input: 
                    - actuator:     name of the actuator to be inserted.
                    - start_time:   Time at which the actuator starts working.
                    - end_time:     Time at which the actuator stops working.
                    - time_on:      Time in minutes that the actuator is on.
                    - time_off:     Time in minutes that the actuator is off. 

                    (this last two variables are only used if the actuator is not always on, 
                     this is useful for example if we have to operate a water pump which does not 
                     need to be always on.

                     if it is always on then time_on and time_off are negative values)

            Output:

            returns a dictionary with the following structure:

            {
                "status":   0 or -1,
                "message":  "message"
            }
        """

        input_check = self.insert_data_watchdog(actuator, start_time, end_time, time_on, time_off)

        if  input_check["status"] == -1:
            return input_check

        # statement for insertion of new data
        insert_statement = insert(self.table).values(actuator_name   = actuator,
                                                     start_time = start_time,
                                                     end_time   = end_time,
                                                     time_on    = time_on,
                                                     time_off   = time_off)
                                                    
        # statement for deletion of previous data
        delete_statement = delete(self.table).where(self.table.c.actuator == actuator)

        with self.engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
            connection.execute(delete_statement)
            connection.execute(insert_statement)

        return {"status": 0, "message": "Data inserted correctly"}


    #-----------------------------------------------------------------------------#
    #                       data check functions                                  #
    #-----------------------------------------------------------------------------#


    def insert_data_watchdog(self, actuator:     str,
                                   start_time:   str,
                                   end_time:     str, 
                                   time_on:      int,
                                   time_off:     int) -> dict:
            
        """
            Function for checking correctness of the data that wants to be inserted.
        """

        # checks if the len of the scring is on accepted len
        if len(actuator) > 60:
            return {"status": -1, "message": "The actuator name is too long."}

        # checks if the actuator exists in the database
        if check_existence_of_actuator(actuator):
            return {"status": -1, "message": "The actuator already exists in the database."}

        # converts the strings to datetime objects to be able to compare them
        try:
            start_time = datetime.strptime(start_time,  '%H:%M:%S')
            end_time   = datetime.strptime(end_time,    '%H:%M:%S')

            if start_time > end_time:
                print("Start time is greater than end time")
                return {"status": -1, "message": "Start time is greater than end time."}

        except ValueError:
            return {"status": -1, "message": "Incorrect time format."}

        # checks time_on and time_off, negative values
        # mean that the actuator is always on, so 
        # no on-off cycles apply to it.
        
        # it's mandatory for the input values to be both 
        # negative, or both positive, if don't then it's bad input

        if ((time_on < 0) and (time_off > 0)) or ((time_on > 0) and (time_off < 0)):
            return {"status": -1, "message": "Incorrect time_on and time_off values."}

        return {"status": 0, "message": "Data is correct"}


    def check_existence_of_actuator(self, actuator) -> bool:

        """
            Checks if the actuator exists in the database.

            Input: 
                    - actuator: name of the actuator to be inserted.
            
            Output:
                    - True,     if the actuator exists in the database.
                    - False,    if the actuator doesn't exist in the database.
        """

        statement = select(self.table).where(self.table.c.actuator == actuator)

        # compiles the statement into a PosgresSQL query string.
        statement = statement.compile(dialect = postgresql.dialect())

        # returns a dataframe with the results
        result = pd.read_sql(statement, self.engine)

        # does not exist
        if result.empty:
            return False

        # exists
        else:
            return True

