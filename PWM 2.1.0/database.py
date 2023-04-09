import mysql.connector

''' 
Establishes connection to the database, 
separated from other modules for easier credentials input, 
since this application is meant to run on localhost.
Returns:
connection: A connection to the database.    
'''

def create_db_connection():
    ''' Takes given input to establish connection to the database, returns connection '''
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your root password",
        database="pwm"
    )
    return connection

