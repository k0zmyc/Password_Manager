import database
from GUI import *
from base64Logic import *
import passgen

'''
This module provides functions for generating passwords, encrypting and decrypting passwords, loading, searching, adding, changing, and deleting passwords in the database.
'''

def generate(length, *entry_fields):
    '''
    Generates a random password with the given length and inserts it into the given entry fields.
    '''
    random_password = passgen.passgen(length=length, punctuation=True, digits=True, letters=True, mixed_case=True, strong=True)

    for entry_field in entry_fields:
        entry_field.delete(0, 'end')
        entry_field.insert(0, random_password)

#**************************************************************************************************************************************************************************************************

def encrypt(key, password):
    '''
    Encrypts the given password with the given encryption key.

    Returns:
    The encrypted password.(str)
    '''
    encoder = Encoder()
    encoder.text = password
    encoder.private_key = key
    encoder.encode()
    return encoder.result

#----------------------------------------

def decrypt(key, password):
    '''
    Decrypts the given password with the given encryption key.

    The decrypted password.(str)
    '''
    encoder = Encoder()
    encoder.text = password
    encoder.private_key = key
    encoder.decode()
    return encoder.result

#**************************************************************************************************************************************************************************************************

def load_passwords(treeview, user_id, encryption_key):
    '''
    Loads all passwords associated with the given user ID and encryption key into the given Treeview.

    Args:
    treeview (Tkinter Treeview): The Treeview to insert the password records into. - Main window(GUI)
    user_id (int): The ID of the user whose passwords to load.
    encryption_key (bytes): The encryption key to use for decryption.

    Returns:
    None.
    '''
    connection = database.create_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id, service, username, password FROM saved_passwords WHERE user_id = %s", (user_id,))
    records = cursor.fetchall()

    # Clear any existing password list entries
    for item in treeview.get_children():
        treeview.delete(item)

    # Populate the password list with decrypted password records
    for record_id, service, username, encrypted_password in records:
        encrypted_password = encrypted_password

        password = decrypt(encryption_key, encrypted_password)

        # Insert the decrypted record into the Treeview
        treeview.insert("", "end", iid=record_id, values=(service, username, password))

    cursor.close()
    connection.close()

#**************************************************************************************************************************************************************************************************

def search_passwords(tree, password_list_frame, search_query, user_id, encryption_key):
    '''
    Searches the database for passwords containing the given search query, and inserts them into the given Treeview.

    Returns:
    None.
    '''
    for item in tree.get_children():
        tree.delete(item)

    connection = database.create_db_connection()
    cursor = connection.cursor()

    search_query = f"%{search_query}%"
    cursor.execute("SELECT service, username, password FROM saved_passwords WHERE user_id = %s AND service LIKE %s", (user_id, search_query))
    records = cursor.fetchall()

    # Insert search results into the Treeview
    for record in records:
        service, username, encrypted_password = record

        password = decrypt(encryption_key, encrypted_password)

        tree.insert("", "end", values=(service, username, password))

#------------------------------------------------------------------------------

def clear_search(search_bar, tree, user_id, encryption_key):
    '''
    Clears the search bar entry and calls method to load passwords, 
    which deletes the search results and loads all corresponding passwords from database.
    '''
    search_bar.delete(0, 'end')
    load_passwords(tree, user_id, encryption_key)

#**************************************************************************************************************************************************************************************************

def check(fields, password_entry, confirm_password_entry):
    '''
    Check if the given fields are not empty and if the given password fields match.
    
    fields is a list of strings

    Returns:
    bool: True if all fields are not empty and the password fields match, False otherwise.    
    '''
    for field in fields:
        if field == "":
            say("Error", "Please fill all fields", "OK")
            return False

    if password_entry != confirm_password_entry:
        say("Error", "Passwords don't match", "OK")
        return False

    return True

#**************************************************************************************************************************************************************************************************

def add_password(self, popup, user_id, service, username, password, confirm_password, encryption_key):
    '''
    Adds a password to the database for the specified user and service.

    Args:
    - self: the current instance of the GUI class
    - popup: the popup window where the user enters their password information
    - user_id: the user ID associated with the password
    - service: the name of the service the password is associated with
    - username: the username associated with the password
    - password: the password to be added
    - confirm_password: the confirmation password to ensure the user has typed their password correctly
    - encryption_key: the key used to encrypt the password

    Returns:
    None
    '''
    if not check([service, username, password, confirm_password], password, confirm_password):
        return

    connection = database.create_db_connection()
    cursor = connection.cursor()

    encrypted_password = encrypt(encryption_key, password)
        
    try:
        cursor.execute("INSERT INTO saved_passwords (user_id, service, username, password) VALUES (%s, %s, %s, %s)", (user_id, service, username, encrypted_password))
        connection.commit()
        popup.destroy()
        load_passwords(self.tree, self.user_id, self.encryption_key)
    except Exception as e:
        print(f"Failed to add password: {e}")
        say("Error","Failed to add password: {e}", "OK")
    finally:
        cursor.close()
        connection.close()

#**************************************************************************************************************************************************************************************************

def change_password(self, popup, tree, user_id, password, confirm_password, encryption_key):
    '''
    Changes the password for a selected service and username in the database.

    Args:
    - self: the current instance of the GUI class
    - popup: the popup window where the user enters their new password information
    - tree: the Treeview displaying the saved passwords
    - user_id: the user ID associated with the password
    - password: the new password to be added
    - confirm_password: the confirmation password to ensure the user has typed their new password correctly
    - encryption_key: the key used to encrypt the new password

    Returns:
    True if the password change was successful, otherwise False.
    
    '''
    selected_item = tree.selection()
    service, username = tree.item(selected_item)['values'][:2]

    if not check([password, confirm_password], password, confirm_password):
        return

    connection = database.create_db_connection()
    cursor = connection.cursor()

    encrypted_password = encrypt(encryption_key, password)

    cursor.execute("UPDATE saved_passwords SET password = %s WHERE user_id = %s AND service = %s AND username = %s", (encrypted_password, user_id, service, username))
    connection.commit()
    connection.close()

    popup.destroy()
    load_passwords(self.tree, self.user_id, self.encryption_key)

    return True

#**************************************************************************************************************************************************************************************************
    
def delete_password(tree, user_id):
    '''
    Deletes a password for a selected service and username from the database.

    Args:
    - tree: the Treeview displaying the saved passwords
    - user_id: the user ID associated with the password

    Returns:
    None
    
    '''
    selected_item = tree.selection()
    if not ask("DELETE PASSWORD?", "Are you sure?"):
        return

    service, username = tree.item(selected_item)['values'][:2]
    
    connection = database.create_db_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM saved_passwords WHERE user_id = %s AND service = %s AND username = %s", (user_id, service, username))
    connection.commit()
    connection.close()

    tree.delete(selected_item)

