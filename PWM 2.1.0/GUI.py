import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from message import say, ask
import login_register_window
from passwords import *

'''
This module implements the GUI for the Password Manager application. The GUI allows users to view, add, modify, and delete their saved passwords.
'''

class GUI:
    def __init__(self, user_id, encryption_key):
        self.user_id = user_id
        self.encryption_key = encryption_key

        self.root = ctk.CTk()
        self.root.title("Password Manager")
        self.root.geometry("650x400")
        self.root.wm_iconbitmap(r"C:\Users\Honza\source\repos\PWM 2.1.0\PWM 2.1.0\icons\pwm_icon.ico")
        self.switchvar = tk.BooleanVar()

 #**************************************************************************************************************************************************************************************************       
        
        # Left frame (1/3 of window) with buttons
        left_frame = ctk.CTkFrame(self.root)
        left_frame.pack(side="left", fill="y")

        # Add "Add Password" and "Delete Password" buttons
        add_password_button = ctk.CTkButton(left_frame, text="Add Password", command=lambda: self.show_add_password_popup())
        add_password_button.pack(pady=5)

        self.change_password_button = ctk.CTkButton(left_frame, text="Change Password", command=self.show_change_password_popup, state="disabled")
        self.change_password_button.pack(pady=5)

        self.delete_password_button = ctk.CTkButton(left_frame, text="Delete Password", command=lambda: delete_password(self.tree, self.user_id), state="disabled")
        self.delete_password_button.pack(pady=5)

        self.logout_button = ctk.CTkButton(left_frame, text="Log Out", fg_color="#b70a0a", hover_color="#9d0d0d", command=self.logout)
        self.logout_button.pack(padx=15, pady=15, side = "bottom")

#**************************************************************************************************************************************************************************************************

        # Right frame (2/3 of window) with search bar and password list
        right_frame = ctk.CTkFrame(self.root)
        right_frame.pack(side="right", fill="both", expand=1)

        # Search bar and search button
        search_bar = ctk.CTkEntry(right_frame, placeholder_text = "service..", width = 350)
        search_bar.grid(row = 0, column = 0, padx = (15,0), sticky="e")
        
        clear_button = ctk.CTkButton(right_frame, text="❌", width=30, height=30, command=lambda: clear_search(search_bar, self.tree, self.user_id, self.encryption_key))
        clear_button.grid(row = 0, column = 1, padx = (1,2), pady = 10, sticky = "w")

        search_button = ctk.CTkButton(right_frame, text="🔍", width=30, height=30, command=lambda: search_passwords(self.tree, self.password_list_frame, search_bar.get(), self.user_id, self.encryption_key))
        search_button.grid(row = 0, column = 2, padx = (0, 25), pady = 10, sticky = "w")

 #**************************************************************************************************************************************************************************************************       
      
        # Password list frame (3/3)
        self.password_list_frame = ctk.CTkFrame(right_frame)
        self.password_list_frame.grid(row=1, column=0, columnspan=3, sticky='nsew')

        right_frame.grid_rowconfigure(1, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)

        # Create a Treeview and configure its columns
        self.tree = ttk.Treeview(self.password_list_frame)
        self.tree["columns"] = ("Service", "Username", "Password")
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("Service", width=150, anchor=tk.W)
        self.tree.column("Username", width=150, anchor=tk.W)
        self.tree.column("Password", width=150, anchor=tk.W)

        #Binding select atribute for treeview
        self.tree.bind("<<TreeviewSelect>>", lambda event: self.update_button_states())

        # Create column headers
        self.tree.heading("#0", text="")
        self.tree.heading("Service", text="Service", anchor=tk.W)
        self.tree.heading("Username", text="Username", anchor=tk.W)
        self.tree.heading("Password", text="Password", anchor=tk.W)

        # Add a scrollbar to the Treeview
        scrollbar = ttk.Scrollbar(self.password_list_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(fill="both", expand=1, padx = 15, pady = 15)

        # Load the user's saved passwords
        load_passwords(self.tree, self.user_id, self.encryption_key)       

        self.root.mainloop()


#**************************************************************************************************************************************************************************************************

    def show_add_password_popup(self):
        '''
        Creates a popup window to add a new password to the database.
        The window contains entry fields for the service name, username, password, and confirm password.
        Clicking the "Save" button runs the add_password function and saves the new password to the database.
    
        '''
        popup = ctk.CTkToplevel()
        popup.title("Add Password")
        popup.geometry("330x280")

        input_frame = ctk.CTkFrame(popup, fg_color = "#143769")
        input_frame.grid(row = 0, sticky = "nsew",padx = 45, pady = 15)

        service_label = ctk.CTkLabel(input_frame, text="Service:")
        service_label.grid(row = 1, column = 0,padx = 5, pady = 5)

        service_entry = ctk.CTkEntry(input_frame)
        service_entry.grid(row = 1, column = 1,padx = 5, pady = 5)

        username_label = ctk.CTkLabel(input_frame, text="Username:")
        username_label.grid(row = 2, column = 0,padx = 5, pady = 5)

        username_entry = ctk.CTkEntry(input_frame)
        username_entry.grid(row = 2, column = 1,padx = 5, pady = 5)

        password_label = ctk.CTkLabel(input_frame, text="Password:")
        password_label.grid(row = 3, column = 0,padx = 5, pady = 5)

        password_entry = ctk.CTkEntry(input_frame, show="*")
        password_entry.grid(row = 3, column = 1,padx = 5, pady = 5)

        confirm_password_label = ctk.CTkLabel(input_frame, text="Confirm PW:")
        confirm_password_label.grid(row = 4, column = 0,padx = 5, pady = 5)

        confirm_password_entry = ctk.CTkEntry(input_frame, show="*")
        confirm_password_entry.grid(row = 4, column = 1,padx = 5, pady = 5)

        show_password_switch = ctk.CTkSwitch(popup, text = "Show passwords", variable=self.switchvar, command=lambda: GUI.show_password(self.switchvar, password_entry, confirm_password_entry))
        show_password_switch.grid()

        generate_button = ctk.CTkButton(popup, text = "Generate strong password", command=lambda: generate(16, password_entry, confirm_password_entry))
        generate_button.grid()
  

        save_button = ctk.CTkButton(
        popup, text="Save",
        command=lambda: add_password(
            self,
            popup,
            self.user_id,
            service_entry.get(),
            username_entry.get(),
            password_entry.get(),
            confirm_password_entry.get(),
            self.encryption_key))

        save_button.grid(pady=5)
        popup.grab_set()

#**************************************************************************************************************************************************************************************************

    def show_change_password_popup(self):
        '''
        Creates a popup window to change the password for a selected service.
        The window contains entry fields for the new password and confirm password.
        Clicking the "Save" button runs the change_password function and updates the password in the database.
    
        '''
        popup = ctk.CTkToplevel()
        popup.title("Change Password")
        popup.geometry("350x350")

        input_frame = ctk.CTkFrame(popup, fg_color = "#143769")
        input_frame.grid(row = 0, sticky = "nsew",padx = 45, pady = 15)

        new_password_label = ctk.CTkLabel(input_frame, text="Password:")
        new_password_label.grid(row = 3, column = 0,padx = 5, pady = 5)

        new_password_entry = ctk.CTkEntry(input_frame, show="*")
        new_password_entry.grid(row = 3, column = 1,padx = 5, pady = 5)

        confirm_password_label = ctk.CTkLabel(input_frame, text="Confirm PW:")
        confirm_password_label.grid(row = 4, column = 0,padx = 5, pady = 5)

        confirm_password_entry = ctk.CTkEntry(input_frame, show="*")
        confirm_password_entry.grid(row = 4, column = 1,padx = 5, pady = 5)

        show_password_switch = ctk.CTkSwitch(popup, text = "Show passwords", variable=self.switchvar, command=lambda: GUI.show_password(self.switchvar, new_password_entry, confirm_password_entry))
        show_password_switch.grid()

        generate_button = ctk.CTkButton(popup, text = "Generate strong password", command=lambda: generate(16, new_password_entry, confirm_password_entry))
        generate_button.grid()

        save_button = ctk.CTkButton(
            popup,
            text="Save",
            command=lambda: change_password(
                self,
                popup,
                self.tree,
                self.user_id,
                new_password_entry.get(),
                confirm_password_entry.get(),
                self.encryption_key))

        save_button.grid(pady=5)
        popup.grab_set()

#**************************************************************************************************************************************************************************************************

    def update_button_states(self):
        '''
        Updates the state of the "Change Password" and "Delete Password" buttons based on whether or not a password is selected in the Treeview.
        If a password is selected, both buttons are enabled. If not, both buttons are disabled.
        '''
        selected_item = self.tree.selection()
        if selected_item:
            self.change_password_button.configure(state="normal")
            self.delete_password_button.configure(state="normal")
        else:
            self.change_password_button.configure(state="disabled")
            self.delete_password_button.configure(state="disabled")

#**************************************************************************************************************************************************************************************************
    
    @staticmethod
    def show_password(show_password_var, *password_entries):
        '''
        Toggles the visibility of passwords in the given entry fields based on the value of the show_password_var variable.
        If show_password_var is True, the passwords are displayed as plain text. If False, they are masked.
        '''
        show_password = show_password_var.get()
        for password_entry in password_entries:
            if show_password:
                password_entry.configure(show="")
            else:
                password_entry.configure(show="*")

#**************************************************************************************************************************************************************************************************
   
    def logout(self):
        '''
        Logs the user out by resetting the user_id and encryption_key variables and destroying the main window.
        Then creates a new Login window for the user to log back in.
        '''
        if ask("LOGOUT", "Are you sure?"):
            self.user_id = None
            self.encryption_key = None
            self.root.destroy()

            login = login_register_window.Login()
            login.log.mainloop()