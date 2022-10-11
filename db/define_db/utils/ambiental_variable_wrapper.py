from sqlalchemy             import MetaData, Table, insert, select
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm         import Session
from sqlalchemy             import Table
from sqlalchemy.dialects    import postgresql

import pandas as pd


# -------------------------------------------
#   base class.
# -------------------------------------------

"""
+-----------------------+--------------------------------+
|   time                |       varname     |   value    |
+-----------------------+--------------------------------+
|                       |                   |            |
| "YYYY/MM/DD %H:%M:%S" |       String      |   Float    |
+-----------------------+--------------------------------+
"""


class AmbientalVariableWrapper():


    def __init__(self, table: Table, engine):
        self.table  = table
        self.engine = engine


    def read_data(self,
                  varname: str,
                  timestamp_start: str,
                  timestamp_end: str) -> pd.DataFrame:

        """
            Reads data from the table, between the specified timestamps.
        """

        statement = select(self.table).\
                    where(self.table.c.varname == varname).\
                    where(self.table.c.time >= timestamp_start).\
                    where(self.table.c.time <= timestamp_end)

        # compiles the statement into a PosgresSQL query string.
        statement = statement.compile(dialect = postgresql.dialect())

        # returns a dataframe with the results
        result = pd.read_sql(statement, self.engine)
        return result


    def insert_data(self, varname: str, value: float) -> dict:

        """
            Inserts data into the table.

            Input:
                    - varname: name of the variable to be inserted.
                    - value:   value of the variable to be inserted.

            Output:

                    returns a dictionary with the following structure:
                    {
                        "stats": 0 or -1,
                        "message": "message"
                    }   
        """

        input_check = self.insert_data_watchdog(value, varname)

        if input_check["stats"] == -1:
            return input_check

        statement = insert(self.table).values(varname = varname, 
                                              value   = value)

        # compiles the statement into a PosgreSQL query string.
        statement = statement.compile(dialect = postgresql.dialect())

        with self.engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
            connection.execute(statement)

        return {"status": 0, "message": "Data inserted successfully."}


    #-------------------------------------------------------------------------#
    #                           checking methods                              #
    #-------------------------------------------------------------------------#

    def insert_data_watchdog(self, value: float, varname: str) -> dict:

        """
            Checks if the input data is valid.

            Input:

                    - value:   value of the variable to be inserted.
                    - varname: name of the variable to be inserted.

            Output:
                    
                    returns a dictionary with the following structure:
                    {
                        "status": 0 or -1,
                        "message": "message"    
                    }
        """

        if not isinstance(varname, str):
            return {"status": -1, "message": "Varname must be a string."}

        if len(varname) > 128:
            return {"status": -1, "message": "Varname must be less than 20 characters."}

        if not check_if_varname_exists(varname):
            return {"status": -1, "message": "Varname does not exist."}

        return {"status": 0, "message": "Data is valid."}


    def check_if_varname_exists(self, varname) -> bool:

        """
            Checks if the varname exists in the table.
        """

        statement = select(self.table).\
                    where(self.table.c.varname == varname)

        # compiles the statement into a PosgreSQL query string.
        statement = statement.compile(dialect = postgresql.dialect())

        with self.engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
            result = connection.execute(statement)

        if result.empty:
            return False
        else:
            return True

    #-------------------------------------------------------------------------#
    #                       initialization methods                            #
    #-------------------------------------------------------------------------#


    def add_variable(self, varname: str) -> dict:

        """
            Adds a new variable to the table.

            Input:

                    - varname: name of the variable to be inserted.

            Output:

                    returns a dictionary with the following structure:
                    {
                        "status": 0 or -1,
                        "message": "message"    
                    }
        """

        #  inserts 0 by default for the new variable.
        value = 0
        input_check = insert_data_watchdog(value, varname)

        if  input_check != {"status": -1, "message": "Varname does not exist."}:
            return input_check

        statement = insert(self.table).values(varname = varname, 
                                              value   = value)

        # compiles the statement into a PosgreSQL query string.
        statement = statement.compile(dialect = postgresql.dialect())

        with self.engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
            connection.execute(statement)

        return {"status": 0, "message": "Varname added successfully."}




