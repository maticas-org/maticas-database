from sqlalchemy import MetaData, Table, Column, DateTime, Float, String, insert, select, delete, update, exists
from datetime import datetime

import pandas as pd
from sqlalchemy.dialects import postgresql

import hashlib
import re
from subprocess import getoutput


email_regex     = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
username_regex  = r'\b^[A-Za-z0-9_-]*$'
numbers_regex   = r'\b\d+$'


"""
    Table Structure:

        +---------+-----------------------+-----------------+------------------+------------------+------------------+---------------------+
        |    id   |   time                |    username     |       email      |     user_db      |     password     |   current api key   |
        +---------+-----------------------+-----------------+------------------+------------------+------------------+---------------------+
        |         |                       |                 |                  |                  |                  |                     |
        |   int   | "YYYY/MM/DD %H:%M:%S" |    "username"   |   "xxx@zzz.aaa"  |     String       |     sha512       |       sha512        |
        +---------+-----------------------+-----------------+------------------+------------------+------------------+---------------------+
"""

class UsersWrapper():


    def __init__(self, table: Table, engine):

        self.table  = table
        self.engine = engine

    def insert_data(self,
                    username:       str,
                    email:          str,
                    password:       str) -> dict:

        """
        Inserts a user into the table.

            INPUT:
                    - username: User name to insert.
                    - email:    User email to insert.
                    - password: User password to insert.

            OUTPUT:
                    - A dictionary with the result of the insertion.
        """

        # deletes white spaces on the sides of the strings
        username, email, password = self.sanitize_input(username, email, password)

        # checks if any field is invalid
        result = self.validate_input(username, email, password)

        if result["status"] == -1:
            return result

        # checks if username and email are available 
        # or if they are already taken
        result = self.check_availability(username, email)

        if result["status"] == -1:
            return result

        # as last step we cannot store the password as rawtext
        # so we will apply a method to cover it.
        password = self.cover_password(password)

        api_key  = self.generate_api_key(username, password)

        # Inserts the value into the table.
        insert_statement = insert(self.table).values(time = datetime.utcnow(),
                                                     username = username, 
                                                     email    = email, 
                                                     user_db  = f'{username}_db',
                                                     password = password, 
                                                     api_key  = api_key)

        with self.engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
            connection.execute(insert_statement)

        return {"status": 0, "message": f'ok. {api_key}'}




    def auth_user_by_username(self, username: str, password: str) -> dict:

        # deletes white spaces on the sides of the strings
        username = self.sanitize_username(username)
        password = self.sanitize_password(password)

        # checks if any field is invalid
        result = self.validate_input(username, "default@gmail.com", password)

        if result["status"] == -1:
            return result


        statement = select(self.table).where(self.table.c.username == username)
        statement = statement.compile(dialect = postgresql.dialect())
        result    = pd.read_sql(statement, self.engine)


        if result.empty:
            return {"status": -1, "message": "user not found."}

        else:
            api_key   = result["api_key"][0]

            password = self.cover_password(password)
            password_check = result["password"][0] == password

            if password_check:
                return {"status": 0, "message": f'ok. {api_key}'}
            else:
                return {"status": -1, "message": "wrong password."}


    def auth_user_by_email(self, email: str, password: str) -> dict:

        # deletes white spaces on the sides of the strings
        email    = self.sanitize_email(email)
        password = self.sanitize_password(password)

        # checks if any field is invalid
        result = self.validate_input("defaultUsername", email, password)

        if result["status"] == -1:
            return result


        statement = select(self.table).where(self.table.c.email == email)
        statement = statement.compile(dialect = postgresql.dialect())
        result    = pd.read_sql(statement, self.engine)


        if result.empty:
            return {"status": -1, "message": "email not found."}

        else:
            api_key   = result["api_key"][0]

            password = self.cover_password(password)
            password_check = result["password"][0] == password

            if password_check:
                return {"status": 0, "message": f'ok. {api_key}'}
            else:
                return {"status": -1, "message": "wrong password."}



    def check_availability(self, 
                           username: str,
                           email:    str) -> dict:

        """
            Reads data from the table.

            INPUT: None.
            OUTPUT: pandas dataframe with the data.
        """

        # dictionary to save the availability of the username name 
        # or the email
        availability = {}

        statement = select(self.table).where(self.table.c.username == username)
        statement = statement.compile(dialect = postgresql.dialect())

        result    = pd.read_sql(statement, self.engine)

        if result.empty:
            availability["status"]  = 0
            availability["message"] = "name available."

        else:
            availability["status"]  = -1
            availability["message"] = "name unavailable."


        statement = select(self.table).where(self.table.c.email == email)
        statement = statement.compile(dialect = postgresql.dialect())

        result    = pd.read_sql(statement, self.engine)

        if result.empty:
            availability["status"]  = 0
            availability["message"] = "email available."

        else:
            availability["status"]  = -1
            availability["message"] = "email unavailable."

        return availability


    def sanitize_input(self, 
                       username:    str, 
                       email:       str, 
                       password:    str):

        """
            INPUT:
                    - username: User name to sanitize.
                    - email:    Email to sanitize.
                    - password: Password to sanitize

            OUTPUT:
                    The input variables sanitized.
        """

        username = self.sanitize_username(username)
        email    = self.sanitize_email(email)
        password = self.sanitize_password(password)

        return username, email, password



    def validate_input(self, 
                       username:    str, 
                       email:       str, 
                       password:    str):

        result = {}
 
        if self.validate_username(username) == False:
            result["status"] = -1 
            result["message"] = "invalid username."

        elif self.validate_email(email) == False:
            result["status"] = -1
            result["message"] = "invalid email."

        elif self.validate_password(password) == False:
            result["status"] = -1
            result["message"] = "invalid password."

        else:
            result["status"] = 0
            result["message"] = "ok."


        return result
        


    def cover_password(self, password: str):

        vowels    = len(re.findall('[aeiou]', password, re.IGNORECASE))
        uppercase = len(re.findall(r'[A-Z]',  password))

        string    = "{0}.{1}.{2}.{1}.{0}".format(vowels, uppercase, password)
        hashhh    = hashlib.sha512( string.encode("utf-8") ).hexdigest()

        return hashhh


    def generate_api_key(self, username, password):

        uppercase_pass = str(len(re.findall(r'[A-Z]',  password)))
        uppercase_user = str(len(re.findall(r'[A-Z]',  username)))

        mem_data = getoutput("free | sed -n '2 p'")
        numbers  = re.findall(numbers_regex, mem_data)
        number   = "".join(numbers)
        
        string = "".join([uppercase_user, uppercase_pass, number, username])
        hashhh    = hashlib.sha512( string.encode("utf-8") ).hexdigest()

        return hashhh



    #---------------------------------------------------------------#

    def validate_username(self, username: str):

        # checks the username
        if (re.fullmatch(username_regex, username)):
            return True

        else:
            return False


    def validate_email(self, email: str):

        # checks the email
        if(re.fullmatch(email_regex, email)):
            return True

        else:
            return False

    def validate_password(self, password: str):

        # checks the password
        if (len(password) < 8) or (len(password) > 60):
            return False

        elif ' ' in password:
            return False

        else:
            return True

    #---------------------------------------------------------------#

    def sanitize_username(self, username: str):
        return username.strip() 

    def sanitize_email(self, email: str):
        return email.strip()

    def sanitize_password(self, password: str):
        return password.strip()



