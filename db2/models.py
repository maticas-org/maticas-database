# db2/models.py
 
import datetime 
import os
from sqlalchemy                 import *
from sqlalchemy.orm             import (scoped_session, sessionmaker, relationship, backref)
from sqlalchemy.ext.declarative import declarative_base
from dotenv                     import load_dotenv

load_dotenv()
conn_string = f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}/{os.getenv("DB_NAME")}'

engine = create_engine(conn_string, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
# We will need this for querying
Base.query = db_session.query_property()


#----------------------------------------  users  -----------------------------------------#
#------------------------------------------------------------------------------------------#
#    id    |    username    |    email    |    api_key    |    passowrd   |  time_created  #
#------------------------------------------------------------------------------------------#
class User(Base):

    __tablename__ = 'users'
    id       = Column(Integer,      primary_key=True)
    username = Column(String(80),   unique = True, nullable = False)
    email    = Column(String(120),  unique = True, nullable = False)
    api_key  = Column(String(256),  unique = True, nullable = False)
    password = Column(String(256),  nullable = False)
    time_created = Column(DateTime, nullable = False, default = datetime.datetime.utcnow)

    user_has_measurements = relationship("Measurement", lazy = 'select')

#-------------------  variables  ------------------#
#--------------------------------------------------#
#    id    |    name    |    units    |    desc    #
#--------------------------------------------------#
class Variable(Base):

    __tablename__ = 'variables'
    id       = Column(Integer,      primary_key=True)
    name     = Column(String(80),   nullable = False)
    units    = Column(String(80),   nullable = False)
    desc     = Column(String(80),   nullable = False)

    variable_has_measurements = relationship("Measurement", lazy = 'select')


#--------------------------  measurements  ------------------------------#
#------------------------------------------------------------------------#
#    id    |    user_id    |    variable_id    |    value    |    time   #
#------------------------------------------------------------------------#
class Measurement(Base):

    __tablename__ = 'measurements'
    id          = Column(Integer,   primary_key=True)
    user_id     = Column(Integer,   ForeignKey('users.id'), nullable = False)
    variable_id = Column(Integer,   ForeignKey('variables.id'), nullable = False)
    value       = Column(Float,     nullable = False)
    time        = Column(DateTime,  nullable = False, default = datetime.datetime.utcnow)


Base.metadata.create_all(engine)











