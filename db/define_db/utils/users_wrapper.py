import pandas as pd
from sqlalchemy.dialects import postgresql

import hashlib
import re
from subprocess import run


email_regex     = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
username_regex  = r'\b^[A-Za-z0-9_-]*$'


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


            OUTPUT:
        """

        # deletes white spaces on the sides of the strings
        username, email, password = self.sanitize_input(username, email, password)

        # checks if any field is invalid
        result = self.validate_input(username, email, password)

        if "invalid" in result.values():
            return result

        # checks if username and email are available 
        # or if they are already taken
        result = self.check_availability(username, email)

        if "taken" in result.values():
            return result

        # as last step we cannot store the password as rawtext
        # so we will apply a method to cover it.
        password = self.cover_password(password)

        api_key  = self.generate_api_key(username, password)

        # Inserts the value into the table.
        insert_statement = insert(self.table).values(username = username, 
                                                     email    = email, 
                                                     user_db  = f'{username}_db'
                                                     password = password, 
                                                     api_key  = api_key)

        with self.engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
            connection.execute(insert_statement)

        return {"status": f'ok. {api_key}'}




    def auth_user_by_username(self, username: str, password: str) -> dict:

        # deletes white spaces on the sides of the strings
        username = self.sanitize_username(username)
        password = self.sanitize_password(password)

        # checks if any field is invalid
        result = self.validate_input(username, "default@gmail.com", password)

        if "invalid" in result.values():
            return result

        statement = select(self.table).where(self.table.c.username == username)
        statement = statement.compile(dialect = postgresql.dialect())
        result    = pd.read_sql(statement, self.engine)
        api_key   = result["api_key"][0]

        print(result)

        if result.empty:
            return {"auth": "User not found."}

        else:
            password = self.cover_password(password)
            password_check = result["password"][0] == password

            return {"auth": f'ok. {api_key}'}


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
            availability["username"] = "free"
        else:
            availability["username"] = "taken"


        statement = select(self.table).where(self.table.c.email == email)
        statement = statement.compile(dialect = postgresql.dialect())
        result    = pd.read_sql(statement, self.engine)

        if result.empty:
            availability["email"] = "free"
        else:
            availability["email"] = "taken"

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
 
        result["username"] = self.validate_username(username)
        result["email"]    = self.validate_email(email)
        result["password"] = self.validate_password(password)


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
        
        string = "".join([uppercase_user, uppercase_pass, number])
        hashhh    = hashlib.sha512( string.encode("utf-8") ).hexdigest()

        return hashhh



    #---------------------------------------------------------------#

    def validate_username(self, username: str):

        # checks the username
        if (re.fullmatch(username_regex, username)):
            return "valid"

        else:
            return "invalid"


    def validate_email(self, email: str):

        # checks the email
        if(re.fullmatch(email_regex, email)):
            return "valid"

        else:
            return "invalid"

    def validate_password(self, password: str):

        # checks the password
        if (len(password) < 8) or (len(password) > 60):
            return "invalid"

        elif ' ' in password:
            return "invalid"

        else:
            return "valid"

    #---------------------------------------------------------------#

    def sanitize_username(self, username: str):
        return username.strip() 

    def sanitize_email(self, email: str):
        return email.strip()

    def sanitize_password(self, password: str):
        return password.strip()


