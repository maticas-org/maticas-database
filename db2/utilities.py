from random     import sample
from subprocess import check_output
from hashlib    import sha256
from datetime   import datetime


def generate_api_key(username: str, 
                     password: str, 
                     email: str):
    
    salt1 = "".join(sample(list(username),  3))
    salt2 = "".join(sample(list(password),  4))
    salt3 = "".join(sample(list(email),     4)) 

    mem_usage = str(check_output('free | grep Mem', shell = True))
    api_key = salt1 + salt2 + salt3 + mem_usage
    api_key = sha256(api_key.encode('utf-8')).hexdigest()

    return api_key

def hash_password(password: str):

    hashed = sha256(password.encode('utf-8')).hexdigest()
    return hashed 

def now():

    current_time  = datetime.utcnow()
    return current_time

def toDateTime(time: str):

    datetime_ =  datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    return datetime_

