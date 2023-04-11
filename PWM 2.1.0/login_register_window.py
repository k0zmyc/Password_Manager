import tkinter as tk
import customtkinter as ctk
import user_auth
from message import say, ask
from GUI import *
from user_auth import register_user, authenticate_user, get_user_id

"""
This module provides the Login class, which allows users to log in or register for the password manager.

Classes:
- Login:
    This class creates a login window, where users can enter their credentials 
    to log in or register for the password manager.
"""

class Login:

    """
    The Login window of the application, where the user can log in or register.

    Methods:
    - __init__(self):
        Initializes the Login window.
    - create_ui(self):
        Creates the user interface for the Login window.
    - login(self):
        Authenticates the user and opens the GUI window.
    - register(self):
        Registers a new user and opens the GUI window.
    """

    def __init__(self):
        """
        Initializes the Login window with a title, size, and icon, and calls create_ui().
        """
        self.log = ctk.CTk()
        self.log.title("Password Manager - Login")
        self.log.geometry("325x250")
        self.log.wm_iconbitmap(r"C:\Users\Honza\source\repos\PWM 2.1.0\PWM 2.1.0\icons\pwm_icon.ico")
        self.create_ui()
        
        database.execute()
                
#**************************************************************************************************************************************************************************************************

    def create_ui(self):
        """
        Creates the user interface for the Login window, including labels, input fields, and buttons(Customtkinter).
        """
        self.input_frame = ctk.CTkFrame(self.log, fg_color = "#143769")
        self.input_frame.grid(row = 0, sticky = "nsew",padx = 45, pady = 15)

        self.username_label = ctk.CTkLabel(self.input_frame, text="Username:")
        self.username_label.grid(row=0, column=0, padx = 10, pady = 5)

        self.username_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Username..")
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        self.password_label = ctk.CTkLabel(self.input_frame, text="Password:")
        self.password_label.grid(row=1, column=0, padx = 10, pady = 5)

        self.password_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Password..", show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        self.or_label = ctk.CTkLabel(self.log, text="or..")
        self.or_label.grid(row=3, column=0, columnspan=2)

        self.login_button = ctk.CTkButton(self.log, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=(5,0))

        self.register_button = ctk.CTkButton(self.log, text="Register", fg_color="#58852d", hover_color="darkgreen", command=self.register)
        self.register_button.grid(row=4, column=0, columnspan=2, pady=(0,10))

        self.switchvar = tk.BooleanVar()
        show_password_switch = ctk.CTkSwitch(self.log, text="Show passwords", variable=self.switchvar, command=lambda: GUI.show_password(self.switchvar, self.password_entry))
        show_password_switch.grid(row=1, column = 0, padx=5, pady=5)
#**************************************************************************************************************************************************************************************************

    def login(self):
        """
        Authenticates the user by checking their username and password against the database.
        If successful, opens the GUI window for the user.
        If unsuccessful, displays an error message using "say" method from "message" module.
        """
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            user_id, encryption_key = authenticate_user(username, password)

            if user_id is not None:
                self.log.destroy()
                GUI(user_id, encryption_key)
            else:
                say("Account doesn't exist!", "Invalid username or password", "Try again!")
        else:
            say("Warning", "Please fill in both fields.", "Try again!")

#**************************************************************************************************************************************************************************************************

    def register(self):
        """
        Registers a new user with the provided username and password.
        If successful, opens the GUI window for the new user.
        If unsuccessful, displays an error message using "say" method from "message" module.
        """
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            if register_user(username, password):
                self.log.destroy()
                user_id, encryption_key = user_auth.get_user_id(username)
                GUI(user_id, encryption_key)
                
            else:
                self.username_entry.delete(0, 'end')
                self.password_entry.delete(0, 'end')
        else:
            say("Warning", "Please fill in both fields.", "Try again!")

#**************************************************************************************************************************************************************************************************

if __name__ == "__main__":
    login = Login()
