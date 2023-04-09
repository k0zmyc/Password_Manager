import tkinter as tk
import customtkinter as ctk



def say(title, message, button_text):

    """
    Displays a message dialog with the given title and message, and a button with the given text.

    Parameters:
        title (str): The title of the message dialog.
        message (str): The message to display.
        button_text (str): The text to display on the button.

    Returns:
        None.
    """
       
    say = ctk.CTkToplevel()
    say.title(title)
    say.geometry("250x150")

    message_label = ctk.CTkLabel(say, text=message)
    message_label.pack(padx=10, pady=10)

    close_button = ctk.CTkButton(say, text=button_text, command=lambda: say.destroy())
    close_button.pack(padx=10, pady=10)

    
    say.grab_set()
    say.wait_window()

#*****************************************************************************************************
def ask(title, message):

    """
    Displays a confirmation dialog with the given title and message, and "YES" and "NO" buttons.

    Parameters:
        title (str): The title of the confirmation dialog.
        message (str): The message to display.

    Returns:
        bool: True if the "YES" button was clicked, False otherwise.
    """

    def yes():
        result.set(True)
        ask.destroy()

    def no():
        result.set(False)
        ask.destroy()

    ask = ctk.CTkToplevel()
    ask.title(title)
    ask.geometry("350x150")


    message_label = ctk.CTkLabel(ask, text=message)
    message_label.pack(padx=10, pady=10)

    button_frame = ctk.CTkFrame(ask)
    button_frame.pack()

    result = tk.BooleanVar()
    result.set(False)

    button1 = ctk.CTkButton(button_frame, text="YES", command=yes)
    button1.grid(row=0, column=0, padx=10, pady=10)

    button2 = ctk.CTkButton(button_frame, text="NO", fg_color="#b70a0a", hover_color="#9d0d0d", command=no)
    button2.grid(row=0, column=1, padx=10, pady=10)

    ask.grab_set()

    ask.wait_window(ask)
        
    return result.get()
