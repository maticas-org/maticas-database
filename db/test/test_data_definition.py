
def title(text: str) -> None:

    """Prints the string centered in a 80 character wide column, and on green color"""

    text = f'\033[1;32m \t {text} \t \033[0m'
    print(text.center(80, " "))

def passed(result: bool) -> None:

    """Prints the string centered in a 80 character wide column, 
    and on blue color if result is True, and red if False"""

    if result:
        text = f'\033[1;34m \t Passed \t \033[0m'
    else:
        text = f'\033[1;31m \t Failed \t \033[0m'

    print(text.center(80, " "))

# this is randomly generated (with real random data, not pseudo-random)
user2_api_key = "983fd75e289796e6ae5a59b87e99e2342e32dbe5be6d53572b86e56c80e3e73161bdca9d5e0f1d79b58c9293305a4c086d24e59f401a5cddd522fa645efa39c8"

#--------------------------------------------------------------------------------#
# This section creates variables for user wrapper testing
#--------------------------------------------------------------------------------#

# ----------------------------------------------------------------------------------------------#
# example users to be added to the database
# for testing input validation and database insertion
example_users_insertion = {
                            # valid user
                            "user1": {"username":   "user1",
                                      "email":      "email@email.com", 
                                      "password":   "ultrasecurepassword"},

                            # duplicarion of username
                            "user11": {"username":   "user1",
                                      "email":      "email@email.com", 
                                      "password":   "ultrasecurepassword"},

                            # user fields with spaces around (yet valid)
                            "user22": {"username":   "   user2 ",
                                       "email":      "   email@gmail.com ",
                                       "password":   "ultrasecurepassword"},

                            # invalid email 
                            "user3": {"username":   "user3",
                                      "email":      "imnotanemail",
                                      "password":   "ultrasecurepassword"},

                            # username with spaces inside 
                            "user33": {"username":   "user 3 hola",
                                       "email":      "imanemail@imanemail.com",
                                       "password":   "ultrasecurepassword"},

                            # username with special characters
                            "user5": {"username":   "user5ññññ",
                                      "email":      "anotheremail@hotmail.com",
                                      "password":   "ultrasecurepassword"},

                            }
user_insertion_output = [0, -1, 0, -1, -1, -1]

# ----------------------------------------------------------------------------------------------#
# for testing user authentication
example_users_auth = {
                        # valid password
                        "user1": {"username":   "user1",
                                  "email":      "email@email.com", 
                                  "password":   "ultrasecurepassword"},

                        # invalid authentication, not the password
                        "user2": {"username":   "user2",   
                                  "email":      "email@gmail.com",
                                  "password":   "this_is_not_the_password_you_are_looking_for"},

                        # inexistent user and email
                        "user3": {"username":   "user69",   
                                  "email":      "email69@gmail.com",
                                  "password":   "this_is_not_the_password_you_are_looking_for"},
                     }

user_auth_output = [0, -1, -1]

# ----------------------------------------------------------------------------------------------#
example_mics_insertion = { 
                            # incorrect api key for the user
                            "mic1": {"username":    "user1",
                                     "api_key":     "1234567890",
                                     "mac_address": "00:00:00:00:00:00",
                                     "mic_name":    "mic1"},

                            # incorrect api key for the user
                            "mic2": {"username":    "user2",
                                     "api_key":     "1234567891234567891234567891234567891234567890A00001234567890",
                                     "mac_address": "00:00:00:00:00:00",
                                     "mic_name":    "mic1"},

                            # unexisten user
                            "mic3": {"username":    "user88",
                                     "api_key":     "1234567891234567891234567891234567891234567890A00001234567890",
                                     "mac_address": "00:00:00:00:00:00",
                                     "mic_name":    "mic1"},
                            # valid user
                            "mic4": {"username":    "user2",
                                     "api_key":     user2_api_key,
                                     "mac_address": "00:00:00:00:00:00",
                                     "mic_name":    "mic1"},
                            # valid user
                            "mic5": {"username":    "user2",
                                     "api_key":     user2_api_key,
                                     "mac_address": "00:00:00:00:00:01",
                                     "mic_name":    "mic0"},
                         }

mics_insertion_output = [-1, -1, -1, 0, 0]



# ----------------------------------------------------------------------------------------------#
# def add_topic(self, usr_name:str, api_key: str, topic: str):

example_topics_insertion = { 
                            # incorrect api key for the user
                            "mic1": {"username":    "user1",
                                     "api_key":     "1234567890",
                                     "topic":       "topic1"},

                            # unexisten user
                            "mic3": {"username":    "user88",
                                     "api_key":     "1234567891234567891234567891234567891234567890A00001234567890",
                                     "topic":       "topic1"},

                            # valid user and api key but invalid topic format
                            "mic4": {"username":    "user2",
                                     "api_key":     "76dfdc01e99f112a664889aee39a30815e9d35c6b37c845eff4e9179440d3311782f9fd7daf0302b0ccd83815cd629dcfa1c517af79c23cc43a2646ee917e12b",
                                     "topic":      "topic1"},

                            # valid input
                            "mic4": {"username":    "user2",
                                     "api_key":     user2_api_key,
                                     "topic":      "anytopic/user2/00:00:00:00:00:00/temperature"},

                            # valid input
                            "mic5": {"username":    "user2",
                                     "api_key":     user2_api_key,
                                     "topic":      "anytopic/user2/00:00:00:00:00:00/humidity"},

                            # inexistent mic mac address
                            "mic5": {"username":    "user2",
                                     "api_key":     user2_api_key,
                                     "topic":      "anytopic/user2/00:00:00:00:00:69/humidity"},

                            # inexistent user
                            "mic6": {"username":    "user2",
                                     "api_key":     user2_api_key,
                                     "topic":      "anytopic/user69/00:00:00:00:00:00/humidity"},
                            
                         }

topics_insertion_output = [-1, -1, -1, 0, 0, -1, -1]


