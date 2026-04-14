#!/usr/bin/env python
import sys
from cs50 import SQL
import re
from getpass import getpass
import os.path
import definitions

if not os.geteuid() == 0: # Only root can run this script
    sys.exit("You can execute this script only with root. Type path to db as argument!")

elif len(sys.argv) == 2 and sys.argv[1] == "--help":
    print("""
For command line: python3 elvinpass.py <DB name> <username> <entry name>
For user interface: python3 elvinpass.py <DB name>
""")
    exit(0)

elif len(sys.argv) < 2 or re.search(".*\.db$", sys.argv[1]) is None:
    print("Usage: you must type path to new or old password database as argument with db extension!")
    exit(1)

elif not os.path.exists(sys.argv[1]):
    file = open(sys.argv[1], "w")
    file.close()
    os.chmod(sys.argv[1], 0o600)
    print("New file created, permissions changed for security reasons.")

db = SQL(f"sqlite:///{sys.argv[1]}")

if len(sys.argv) == 2:
    if not definitions.there_is_users(db):
        answer = input("Create a new user for DB? ")
        if re.search("(?i)y", answer) is not None:
            username, password = definitions.create_user_and_table_in(db)
        else:
            print("Exit from interface, answer is negative!")
            exit(0)
    else:
        username = input("Type username or create a new one (Type new): ")
        if re.search("(?i)^new$", username) is not None:
            username, password = definitions.create_user_and_table_in(db)
        else:
            password = getpass("Type your password: ")
            if not definitions.authenticate_user(db, username, password):
                print("Authentication failed, invalid username or password")
                exit(1)
        while True:
            answer = definitions.starting_main_interface(db, username, password)

else:
    if len(sys.argv) > 4:
        print("Unexpected number of arguments!")
        exit(1)
    else:
        password = getpass("Type your password: ")
        if definitions.authenticate_user(db, sys.argv[2], password):
            definitions.decrypt_and_copy_to_buffer_for_command(db, sys.argv[3], password)
            exit(0)
