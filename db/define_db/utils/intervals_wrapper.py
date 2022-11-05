from sqlalchemy import MetaData, Table, Column, DateTime, Float, String, insert, select, delete, update 
from datetime import datetime

import pandas as pd
from sqlalchemy.dialects import postgresql


"""
    Table Structure:

    +-----------------------+-----------------+--------------------+---------------------+------------------+------------------+
    |   time                |   variable      |   min_acceptable   |   max_acceptable    |   min_optimal    |   max_optimal    |
    +-----------------------+-----------------+--------------------+---------------------+------------------+------------------+
    |                       |                 |                    |                     |                  |                  |
    | "YYYY/MM/DD %H:%M:%S" | "variable_name" |       number       |       number        |       number     |       number     |
    +-----------------------+-----------------+--------------------+---------------------+------------------+------------------+
"""


class IntervalsWrapper():

    def __init__(self, table: Table, engine):

        self.table  = table
        self.engine = engine


    def insert_data(self,
                    variable:               str,
                    acceptable_interval:    tuple,
                    optimal_interval:       tuple) -> int:

            """
            Inserts data into the table.
            
                INPUT: 
                        variable:    str with the name of the variable.
                        acceptable_interval: tuple with the acceptable interval. with data type: (float, float).
                                             it has the shape (min_value, max_value).
                        optimal_interval:    tuple with the optimal interval. with data type: (float, float).
                                             it has the shape (min_value, max_value).

                OUTPUT: 0 if everithing went ok,
                        -1 if there was an error.
            """

            if self.insert_data_watchdog(acceptable_interval, optimal_interval) == -1:
                return -1
    
            # Deletes the previous value of the variable if it exists.
            delete_statement = delete(self.table).where(self.table.c.variable == variable)


            # Inserts the value into the table.
            insert_statement = insert(self.table).values(time = datetime.utcnow(),
                                                         variable = variable,
                                                         min_acceptable = acceptable_interval[0],
                                                         max_acceptable = acceptable_interval[1],
                                                         min_optimal = optimal_interval[0],
                                                         max_optimal = optimal_interval[1])
            

    
            with self.engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
                connection.execute(delete_statement)
                connection.execute(insert_statement)

            return 0


    def read_all_data(self) -> pd.DataFrame:
        """
            Reads all data from the table.

            INPUT:  None
            OUTPUT: pandas dataframe with the data.
        """

        statement = select(self.table)

        # compiles the statement into a PosgresSQL query string.
        statement = statement.compile(dialect = postgresql.dialect())

        # returns a dataframe with the results
        result = pd.read_sql(statement, self.engine)
        return result


    def read_data(self, variable: str) -> pd.DataFrame:

        """
            Reads data from the table.

            INPUT: None.
            OUTPUT: pandas dataframe with the data.
        """

        statement = select(self.table).where(self.table.c.variable == variable)

        # compiles the statement into a PosgresSQL query string.
        statement = statement.compile(dialect = postgresql.dialect())

        # returns a dataframe with the results
        result = pd.read_sql(statement, self.engine)
        return result


    def insert_data_watchdog(self,
                             acceptable_interval:   tuple,
                             optimal_interval:      tuple) -> int:

        """
            Function for checking correctness of the data that wants to be inserted.

            INPUT: acceptable_interval: tuple with the acceptable interval. with data type: (float, float).
                                        it has the shape (min_value, max_value).

                   optimal_interval:    tuple with the optimal interval. with data type: (float, float).
                                        it has the shape (min_value, max_value).

            OUTPUT: 0 if everithing went ok,
                    -1 if there was an error.
        """

        if acceptable_interval[0] >= acceptable_interval[1]:
            return -1 

        if optimal_interval[0] >= optimal_interval[1]:
            return -1 

        if (acceptable_interval[0] > optimal_interval[0]) or (acceptable_interval[1] < optimal_interval[1]):
            return -1

        return 0 


