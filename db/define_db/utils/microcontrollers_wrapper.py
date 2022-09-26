from sqlalchemy import MetaData, Table, Column, DateTime, Float, String, insert, select, delete, update 
from datetime import datetime

import pandas as pd
from sqlalchemy.dialects import postgresql

class MicrocontrollersWrapper():

    def __init__(self, table: Table, engine):

        self.table = table
        self.engine = engine



