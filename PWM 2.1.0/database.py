import mysql.connector

''' 
Establishes connection to the database, 
separated from other modules for easier credentials input, 
since this application is meant to run on localhost.
Returns:
connection: A connection to the database.    
'''

def create_db_connection():
    '''
    Takes given input to establish connection to the database, returns connection.
    '''
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="dpT84d-tgnRDY",
        database="pwm"
    )
    
    return connection

def execute():
    '''
    Creates a database with the tables needed for running this code.
    '''
    connection = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "dpT84d-tgnRDY"
        )
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS pwm")

    cursor.close() 
    connection.close()

    connection = create_db_connection()
    cursor = connection.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS user_credentials (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255) NOT NULL UNIQUE, hashed_password BLOB NOT NULL, salt BLOB NOT NULL, encryption_key BLOB NOT NULL)")

    cursor.execute("CREATE TABLE IF NOT EXISTS saved_passwords (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT NOT NULL, platform VARCHAR(255) NOT NULL, username VARCHAR(255) NOT NULL, password TEXT NOT NULL, FOREIGN KEY (user_id) REFERENCES user_credentials(id))")

    cursor.close() 
    connection.close()