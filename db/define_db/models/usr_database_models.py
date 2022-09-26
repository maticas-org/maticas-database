from sqlalchemy import MetaData, Table, Column, DateTime, Time, Float, Integer, String, ForeignKey, insert, select, delete
from datetime import datetime
import pandas as pd

from sqlalchemy.dialects        import postgresql
from sqlalchemy.orm             import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


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

    """
    Table Structure:

        +-----------------------+--------------------------------+
        |   time                |       varname     |   value    |
        +-----------------------+--------------------------------+
        |                       |                   |            |
        | "YYYY/MM/DD %H:%M:%S" |       String      |   Float    |
        +-----------------------+--------------------------------+
    """

    __tablename__ = 'ambiental_variables'

    time    = Column(DateTime,              nullable = False,   default = datetime.utcnow, primary_key = True)
    varname = Column(String(128),           nullable = False,   primary_key = True)
    value   = Column(Float(precision = 3),  nullable = False)


    def __repr__(self):
        return f"<AmbientalVaraible {self.varname}>"



