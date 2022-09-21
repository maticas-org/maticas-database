from sqlalchemy import MetaData, Table, Column, DateTime, Time, Float, Integer, String, ForeignKey, insert, select, delete
from datetime import datetime
import pandas as pd

from sqlalchemy.dialects import postgresql
from sqlalchemy.orm      import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):

    """
        Users table, this table contains the users of the application.
        the user's password is hashed.

        Also contains the user's database name, which is used to store the user's specific data.
    """

    __tablename__ = 'users'

    id       = Column(Integer,          autoincrement = "auto",         primary_key = True)
    time     = Column(DateTime,         default     = datetime.utcnow,  nullable = False)
    username = Column(String(128),      unique      = True,             nullable = False)
    email    = Column(String(128),      unique      = True,             nullable = False)
    user_db  = Column(String(132),      unique      = True,             nullable = False)
    password = Column(String(128),      nullable    = False)
    api_key  = Column(String(128),      unique      = True,             nullable = False)

    # every user has many microcontrollers 
    usr_mics  = relationship("Microcontrollers")

    # every user has many mqtt topics which send data to the server
    usr_topics  = relationship("MQTTTopics")

    def __repr__(self):
        return f"<User {self.username}>"


class Microcontrollers(Base):
    
    """
        Microcontrollers table, this table contains the microcontrollers that the user has registered.
    """

    __tablename__ = 'microcontrollers'

    usr_id      = Column(Integer,       ForeignKey('users.id'),     primary_key = True)
    time        = Column(DateTime,      nullable = False,           default     = datetime.utcnow)
    name        = Column(String(128),   nullable = True)
    mac_address = Column(String(20),    unique = True,              primary_key = True )

    def __repr__(self):
        return f"<Microcontroller {self.name}>"




class MQTTTopics(Base):

    """
        MQTTTopics table, this table contains the topics that the user has registered.
    """
    __tablename__ = 'mqtt_topics'

    usr_id  = Column(Integer,       ForeignKey('users.id'), primary_key = True)
    topic   = Column(String(128),   unique = True,          primary_key = True)

    def __repr__(self):
        return f"<Microcontroller {self.topic}>"


class Actuator(Base):

    __tablename__ = 'actuators'

    actuator_id     = Column(Integer,       autoincrement = "auto", primary_key = True)
    time            = Column(DateTime,      nullable = False,       default = datetime.utcnow)
    actuator_name   = Column(String(128),   nullable = False)
    start_time      = Column(Time,          nullable = False)
    end_time        = Column(Time,          nullable = False)
    time_on         = Column(Float,         nullable = False)
    time_off        = Column(Float,         nullable = False)


    def __repr__(self):
        return f"<Actuator {self.actuator_name}>"


class AmbientalVaraible(Base):

    __tablename__ = 'ambiental_variables'

    time    = Column(DateTime,              nullable = False,   default = datetime.utcnow, primary_key = True)
    varname = Column(String(128),           nullable = False,   primary_key = True)
    value   = Column(Float(precision = 3),  nullable = False)


    def __repr__(self):
        return f"<AmbientalVaraible {self.varname}>"



