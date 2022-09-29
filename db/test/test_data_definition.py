
#--------------------------------------------------------------------------------#
# This section creates variables for user wrapper testing
#--------------------------------------------------------------------------------#

# example users to be added to the database
# for testing input validation and database insertion
example_users = {
                    "user1": {"username":   "user1",
                              "email":      "email@email.com", 
                              "password":   "ultrasecurepassword"},

                    "user2": {"username":   "user2",
                              "email":      "email@gmail.com",
                              "password":   "ultrasecurepassword123"},

                    "user22": {"username":   "user2 ",
                               "email":      " email@gmail.com ",
                               "password":   "ultrasecurepassword"},

                    "user3": {"username":   "user3",
                              "email":      "imnotanemail",
                              "password":   "ultrasecurepassword"},

                    "user4": {"username":   "user4",
                              "email":      "anotheremail@protonmail.com",
                              "password":   "ultrasecurepassword"},

                    "user44": {"username":   "user4",
                              "email":      "anotheremail@",
                              "password":   "this_is_not_the_password_you_are_looking_for"},

                    "user5": {"username":   "user5ññññ",
                              "email":      "anotheremail@hotmail.com",
                              "password":   "ultrasecurepassword"},

                    "user55": {"username":   "+",
                              "email":      "anotheremail12@hotmail.com",
                              "password":   "ultrasecurepassword"},

                }

output_for_example_users_insertion = (0, 0, -1, -1, -1, -1, -1, -1, -1)
output_for_example_users_auth_by_username = (0, 0, 0, -1, 0, -1, -1, -1, -1)



