import bcrypt
import database
from message import say
import os
#from base64 import b64encode


'''
This module provides functions for registering users, authenticating users, and getting the user ID and encryption key.
'''


def register_user(username, password):
    '''
    register_user(username: str, password: str) -> bool:
    Registers a new user with the given username and password. Returns True if successful, False otherwise.
    '''
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    encryption_key = os.urandom(32)

    connection = database.create_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM user_credentials WHERE username = %s", (username,))
    result = cursor.fetchone()

    if result[0] > 0:
        say("Error!", "Username, already exists!", "Try again")
        return False
    
    
    else:
        try:
            cursor.execute("INSERT INTO user_credentials (username, hashed_password, salt, encryption_key) VALUES (%s, %s, %s, %s)", (username, hashed_password, salt, encryption_key))

            connection.commit()
            return True

        except mysql.connector.Error as e:
            #print(f"Failed to register user: {e}")
            say("Error", "Failed to register user: {e}", "OK")
            return False

        finally:
            cursor.close()
            connection.close()

#**************************************************************************************************************************************************************************************************

def get_user_id(username):
    '''
    get_user_id(username: str) -> tuple:
    Returns a tuple containing the user ID and encryption key for the given username.
    '''
    connection = database.create_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id, encryption_key FROM user_credentials WHERE username = %s", (username,))
    user_id, encryption_key = cursor.fetchone()

    return user_id, encryption_key

#**************************************************************************************************************************************************************************************************

def authenticate_user(username, password):
    '''
    authenticate_user(username: str, password: str) -> tuple:
    Authenticates a user with the given username and password. Returns a tuple containing the user ID and encryption key if successful, or (None, None) otherwise.
    '''
    connection = database.create_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id, hashed_password, salt, encryption_key FROM user_credentials WHERE username = %s", (username,))
    result = cursor.fetchone()

    if result:
        user_id, hashed_password, salt, encryption_key = result
        if bcrypt.checkpw(password.encode('utf-8'), bytes(hashed_password)):
            # Return the user_id and encryption_key
            return user_id, encryption_key
        else:
            return None, None



