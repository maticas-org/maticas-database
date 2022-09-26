from sqlalchemy             import MetaData, Table
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm         import Session
from sqlalchemy             import Table

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


    def watch_dog(self, value) -> float:
        if value < 0:
            return -1


    def insert_data(self, value: float) -> int:

        """
            Inserts data into the table.

            if any error with the data it returns -1, 
            if a successfully inserted data it returns 0.
        """

        if watch_dog(value) == -1:
            return -1

        statement = insert(self.table).values(value)

        with self.engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
            connection.execute(statement)

        return 0



