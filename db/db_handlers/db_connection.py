from sqlalchemy         import MetaData, Table, Column, DateTime, Float, insert, select, delete
from sqlalchemy_utils   import database_exists, create_database
from sqlalchemy         import create_engine

import datetime
import pytz
import psycopg2
import pandas as pd

from sys        import path
from os.path    import abspath, dirname

# the directory where the database is defined to the path
root_dir = dirname(dirname(abspath(__file__)))
path.append( root_dir + "/define_db" )


#
# this is a database connection class 
# specific to some user database, now as this is an API 
# and we have many users, we will have to create a class
# kinda "user_data_manager" to manage the database connection
# for each user.
# 
# that basically implies having a new database of user data
# and one instance of the class "DbConnection" for each user.
#

from tables_utilities import load_data_tables


class DbConnection():

    #-----------------------------------------------#
    # Initialization and configuration of the class #
    #-----------------------------------------------#

    def __init__(self, 
                 db_host: str,
                 db_name: str,
                 db_user: str,
                 db_password: str,
                 db_sslmode: str ):

        print("Starting database connection...")

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

        print("Done creating database connection.")
        print("-"*60)
            

    def configure_connection(self) -> None:

        """
        """

        # verify if the database exists, if not, creates it
        self.verify_database()

        # load the tables from the database, if they don't exist, it creates them
        self.all_tables = load_data_tables(self.engine, self.metadata)
        self.var_table = self.all_tables["ambiental_variables"]

        self.intervals_table = self.all_tables["variables_intervals"]
        self.actuators_table = self.all_tables["actuators"]

        # now I need to override the initialization of a table
        # and allow for the insertion of an already created table in the object
        # Variable, in order to unlock all the previously implemented features.

        print("Done setting up the configuration.")
        print("-"*60)


    #-----------------------------------------------------------#
    # Functions to read and write the ambiental variable tables #
    #-----------------------------------------------------------#



    def write_data(self, value: float, varname: str, verbose = False) -> None:

        """
        INPUTS:
                value:      Float to be written in the database.

                varname:    Name of the variable which has a measurement to be written. 

                verbose:    Option to show the output/status of the query.
                            Exit code 0, means no problem and -1 means there was a problem.
        OUTPUT:
                None. This function writes the data in the table corresponding to the alias.
        """

        result = self.var_table.insert_data(varname = varname, value = value)
        print(result)

        if verbose:
            print("Inserted data in table {0}, with exit code: {1}".format(table_name, result))

        return result


    def read_data(self, varname: str, timestamp_start: str, timestamp_end: str) -> dict:

        """
        INPUTS:
                - varname:         The table where the data will be read.
                - timestamp_start:    Start timestamp of the data to be read. It's format is 
                                      'YYYY-MM-DD HH:MM:SS'.
                - timestamp_end:      End timestamp of the data to be read. It's format is
                                      'YYYY-MM-DD HH:MM:SS'.
                
        OUTPUT:
                Returns a pandas dataframe with this shape:
                +-----------------------+---------------+-----------------+
                |   time                |   varname     |   column_name   |
                +-----------------------+---------------+-----------------+
                |                       |               |                 |
                | "YYYY/MM/DD %H:%M:%S" |   Strig       | decimal_number  |
                +-----------------------+---------------+-----------------+
        """

        data = self.var_table.read_data(varname = varname,
                                        timestamp_start = timestamp_start,
                                        timestamp_end = timestamp_end).to_dict()

        data["time"] = self.convert2datetime( data["time"] ) 
    
        return data



    ############################################################# 
    #--------------------------------------------------------------#
    # Functions to read and write the ambiental variable, interval #
    # of each variable the user is interested to track.            #
    #--------------------------------------------------------------#

    def write_ambiental_variable_interval(self, 
                                          variable: str, 
                                          acceptable_interval: tuple,
                                          optimal_interval:    tuple, 
                                          verbose = False) -> dict:

        """
        INPUTS:
                - variable:            Ambiental variable for which the intervals will be written.
                - acceptable_interval: Tuple with the acceptable interval, that is a range of 
                                       acceptable values for the ambiental variable.
                - optimal_interval:    Tuple with the optimal interval, that is a range of
                                       optimal values for the ambiental variable.
                - verbose:             Mainly for debugging purposes.
        OUTPUT:
                None. This function writes the data in the table corresponding to the alias.
        """

        result = self.intervals_table.insert_data(variable = variable,
                                                  acceptable_interval = acceptable_interval,
                                                  optimal_interval    = optimal_interval)

        if verbose:
            print("Inserted data in table {0}, with exit code: {1}".format(variable, result))

        return result



    def read_ambiental_variable_interval(self, variable: str) -> dict:

        """
        INPUTS:
                - variable:  Ambiental variable for which the intervals will be read.

        OUTPUT:
                Returns a pandas dataframe with this shape: 
                +-----------------------+-----------------+--------------------+---------------------+------------------+------------------+
                |   time                |   variable      |   min_acceptable   |   max_acceptable    |   min_optimal    |   max_optimal    |
                +-----------------------+-----------------+--------------------+---------------------+------------------+------------------+
                |                       |                 |                    |                     |                  |                  |
                | "YYYY/MM/DD %H:%M:%S" | "variable_name" |       number       |       number        |       number     |       number     |
                +-----------------------+-----------------+--------------------+---------------------+------------------+------------------+
        """

        data = self.intervals_table.read_data(variable = variable).to_dict()

        data["time"] = self.convert2datetime( data["time"] ) 

        return data

    ############################################################# 
    #------------------------------------------------------------#
    # Functions to read and write the settings for the actuators #
    # that is: the definition of when an actuator starts working,#
    # when it stops working. And if necessary the time it should #
    # be on, and off.                                            #
    #------------------------------------------------------------#


    def write_actuators_configuration(self, actuator_name:  str,
                                            start_time:     str,
                                            end_time:       str,
                                            on_time:        int,
                                            off_time:       int,
                                            verbose = False) -> int:

        """
            INPUT:
                    - actuator_name:    Name of the actuator for which the configuration will be written.
                    - start_time:       Time when the actuator starts working.
                    - end_time:         Time when the actuator stops working.
                    - on_time:          Number of minutes in which the the actuator is on.
                    - off_time:         Number of minutes in which the the actuator is off.

            OUTPUT:
                    None. This function writes the data in the table corresponding to the alias.
        """
        

        result = self.actuators_table.insert_data(actuator   = actuator_name,
                                                  start_time = start_time,
                                                  end_time   = end_time,
                                                  time_on    = on_time,
                                                  time_off   = off_time)

        return result
        

    def read_actuators_configuration(self, actuator_name: str) -> dict:

        """
            INPUT:
                    - actuator_name:    Name of the actuator for which the configuration will be read.

            OUTPUT:
                    Returns a pandas dataframe with this shape:
                    +-----------------------+-----------------+----------------+---------------+--------------+------------------+
                    |   time                |   actuator      |   start_time   |   end_time    |   time_on    |   time_off       |
                    |-----------------------+-----------------+----------------+---------------+--------------+------------------+
                    |                       |                 |                |               |              |                  |
                    | "YYYY/MM/DD %H:%M:%S" | "actuator_name" |   "%H:%M:%S"   |  "%H:%M:%S"   |    nminutos  |     nminutos     |
                    +-----------------------+-----------------+----------------+---------------+--------------+------------------+
        """

        data = self.actuators_table.read_data(actuator = actuator_name).to_dict()
        data["time"] = self.convert2datetime(data["time"])
        data["start_time"] = self.convert2time(data["start_time"])
        data["end_time"]   = self.convert2time(data["end_time"])

        return data

    #---------------------------------------#
    #           create operations
    #---------------------------------------#

    def verify_database(self) -> None:

        if not database_exists(self.engine.url):

            create_database(self.engine.url)
            print('Database created!')

        print('Database found!')


    #---------------------------------------#
    #               utils
    #---------------------------------------#

    def convert2datetime(self, time: dict):
        
        for key, value in time.items():
            time[key] = value.strftime("%Y/%m/%d %H:%M:%S")

        return time
        

    def convert2time(self, time: dict):
        """
        INPUT:  Dictionary with the shape: {0: "datetime.time(x, x, x)"}
        OUTPUT: Dictionary with the shape: {0: "HH:MM:SS"}
        """

        for key, value in time.items():
            time[key] = value.strftime("%H:%M:%S")

        return time




