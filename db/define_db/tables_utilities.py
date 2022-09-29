from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm         import Session
from sqlalchemy             import Table

from sys import path
from os.path import abspath, dirname

current_file_directory = dirname(abspath(__file__))
path.append( current_file_directory + "/utils")
path.append( current_file_directory + "/models")

# imports database tables definitions 
from utils.users_wrapper              import UsersWrapper
from utils.microcontrollers_wrapper   import MicrocontrollersWrapper
from utils.topics_wrapper             import TopicsWrapper
from utils.ambiental_variable_wrapper import AmbientalVariableWrapper
from utils.intervals_wrapper          import IntervalsWrapper
from utils.actuators_wrapper          import ActuatorsWrapper



def find_existent_tables(engine = None) -> list:

    """
        Finds the existent tables in the database.
    """

    base = automap_base()
    base.prepare(engine, reflect=True)
    
    # returns the list of the existent tables
    return base.classes.keys()


#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#


def load_all_tables(engine = None, metadata = None) -> dict:

    """
        Loads all the tables in the database.
    """

    # dictionary to store the loaded or generated tables
    all_tables = load_users_tables(engine = engine, metadata = metadata)
                                     
    return all_tables



#--------------------------------------------------------------------------------------------#
#                           Particular user database tables utilities                        #
#--------------------------------------------------------------------------------------------#

def create_unexistent_user_tables(engine = None, metadata = None) -> None:

    """
        Creates the user tables that are not in the database.
    """

    table_name = find_existent_tables(engine)
    
    # checks if there are unexistent tables
    lack_of_tables = len( set(table_name).symmetric_difference( set(["users", "microcontrollers", "mqtt_topics"])) ) > 0

    if lack_of_tables:
        print("The database is missing some tables. Default table creation will be used.")

        from usrs_model import Base
        Base.metadata.create_all(engine)

    return 



def load_users_tables(engine = None, metadata = None) -> dict:

    """
        Loads all the the tables relative to user information 
        and returns a dictionary with the tables.
    """

    create_unexistent_user_tables(engine = engine, metadata = metadata)

    tables = {'users': None, 'microcontrollers': None, 'topics': None}

    # loads an instance of the users table
    users_table = Table('users',            
                        metadata,
                        autoload = True,
                        autoload_with = engine)

    # extends the table functionalities
    users_table = UsersWrapper(table  = users_table, 
                               engine = engine)

    tables["users"] = users_table


    # loads an instance of the microcontrollers table
    mics_table = Table('microcontrollers',            
                        metadata,
                        autoload = True,
                        autoload_with = engine)

    # extends the table functionalities
    mics_table = MicrocontrollersWrapper(table  = mics_table,
                                         engine = engine)

    tables["microcontrollers"] = mics_table

    # loads an instance of the mqtt_topics table
    topics_table = Table('mqtt_topics',            
                          metadata,
                          autoload = True,
                          autoload_with = engine)

    # extends the table functionalities
    topics_table = TopicsWrapper(table  = topics_table,
                                 engine = engine)

    tables["topics"] = topics_table


    return tables


#--------------------------------------------------------------------------------------------#
#                           Particular user database tables utilities                        #
#--------------------------------------------------------------------------------------------#

def create_unexistent_data_tables(engine = None, metadata = None) -> None:

    """
        Creates the user tables that are not in the database.
    """

    table_names = find_existent_tables(engine)
    
    # checks if there are unexistent tables
    lack_of_tables = len( set(table_names).symmetric_difference( set(["actuators", "ambiental_variables", "variables_intervals"])) ) > 0

    if lack_of_tables:
        print("The database is missing some tables. Default table creation will be used.")

        from usr_database_models import Base
        Base.metadata.create_all(engine)

    return 

def load_data_tables(engine = None, metadata = None):

    create_unexistent_data_tables(engine = engine, metadata = metadata)

    tables = {'actuators': None, 'ambiental_variables': None, 'variables_intervals': None}

    # loads an instance of the users table
    actuators_table = Table('actuators',
                             metadata,
                             autoload = True,
                             autoload_with = engine)

    # extends the table functionalities
    actuators_table = ActuatorsWrapper(table  = actuators_table, 
                                       engine = engine)

    tables["actuators"] = actuators_table


    # loads an instance of the ambiental variables table
    ambiental_var_table = Table('ambiental_variables',            
                                 metadata,
                                 autoload = True,
                                 autoload_with = engine)

    # extends the table functionalities
    ambiental_var_table = AmbientalVariableWrapper(table  = ambiental_var_table,
                                                   engine = engine)

    tables["ambiental_variables"] = ambiental_var_table

    # loads an instance of the mqtt_topics table
    var_intervals_table = Table('variables_intervals',            
                                 metadata,
                                 autoload = True,
                                 autoload_with = engine)

    # extends the table functionalities
    var_intervals_table = IntervalsWrapper(table  = var_intervals_table,
                                           engine = engine)

    tables["variables_intervals"] = var_intervals_table


    return tables









