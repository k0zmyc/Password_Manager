# Password Manager

This password manager is a Python application that allows users to store and manage their passwords securely.
The application includes user authentication, password encryption, and a graphical interface.

## Table of Contents
1. [Application Structure](##Application structure)
2. [Installation](##Installation)
3. [Usage](##Usage)
4. [Features](##Features)
5. [Example](##Example)

## Aplication structure

* database.py: Establishes a connection to the database.
* base64Logic.py: Contains the Encoder class for encoding and decoding text using a private key and Base64 encoding.
* user_auth.py: Provides functions for registering and authenticating users, as well as obtaining the user ID and encryption key.
* massage.py Provides methods for alerting the user when error is encountered of when confirmation is needed.
* login_register_window.py: Contains the Login class that manages the login and registration interface.
* passwords.py Provides methods for generating strong passwords, encryption and decryption and working withe the database.
* GUI.py Contains the GUI class that includes several method for managing GUI(Graphical User Interface) such as main window of the application,
 or pop-up windows for user interaction.
* main.py: The main file that starts the application.



## Istallation
To run this application, you'll need to have Python 3.6 or higher installed. Additionally, you'll need to install the following packages using pip:


@requirements.txt

mysql-connector-python==8.0.32
customtkinter==5.1.2
bcrypt==4.0.1
passgen==1.1.1


## Usage
Ensure you have a MySQL server running with the appropriate database schema (not provided in this README).
Modify the database.py file to include your MySQL server's connection details (host, user, password, and database name).
Run main.py to start the application.
Use the graphical interface to register a new user or log in to an existing account.
Please note that this application is meant to run on localhost and is not intended for deployment on a public server.


## Freatures


## Example
