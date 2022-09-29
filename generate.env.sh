#!/bin/bash

initiate_dotenv(){
    echo "$1" > .env
}

append_to_dotenv(){
    echo "$1" >> .env
}

initiate_dotenv "DB_HOST='localhost'"
append_to_dotenv "DB_NAME='maticas'"
append_to_dotenv "DB_USER='dave'"
append_to_dotenv "DB_PASSWORD='0000'"
append_to_dotenv "DB_SSLMODE='disable'"

append_to_dotenv "USR_DB_HOST='localhost'"
append_to_dotenv "USR_DB_NAME='maticas_users'"
append_to_dotenv "USR_DB_USER='dave'"
append_to_dotenv "USR_DB_PASSWORD='0000'"
append_to_dotenv "USR_DB_SSLMODE='disable'"


