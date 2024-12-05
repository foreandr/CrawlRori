import customtkinter as ctk
from tkinter import messagebox
import json
import func
import hyperSel.colors_utilities
import hyperSel.log_utilities
import hyperSel.selenium_utilities
import crud_credentials
import custom_log
import hyperSel
import validation_rules
import tkinter as tk
from tkinter import ttk
from difflib import SequenceMatcher
import customtkinter as ctk
import single_url_crawl
import threading
import time
import gui_algemeen
from tkinter import Scrollbar

import gui_credenitals

# Test mode flag to skip login
test_mode = True
admin=None
# Function to validate login and open appropriate page
def validate_login(username, password, root, credentials):
    # Check if username and password match for admin accounts
    for admin in credentials["admin_accounts"]:
        if username == admin["username"] and password == admin["password"]:
            messagebox.showinfo("Login Success", f"Logged in as Admin: {username}")
            open_main_window(root, is_admin=True)
            return

    # Check if username and password match for user accounts
    for user in credentials["user_accounts"]:
        if username == user["username"] and password == user["password"]:
            messagebox.showinfo("Login Success", f"Logged in as User: {username}")
            open_main_window(root, is_admin=False)
            return

    messagebox.showerror("Login Failed", "Incorrect username or password.")

# Separate function to add the Search tab
def display_data(data, parent):
    recording_tool_data = data["recording_tool"]
    control_tool_data = data["control_tool"]

    # Fetch recording tool data for each tab type
    (
        algemeen_data,
        omgevingskenmerken_data,
        gebouwen_data,
        ruimtes_data,
        schades_data,
        bijlagen_data,
        samenvatting_data,
    ) = func.get_recording_tool_data(recording_tool_data)

    # Clear any previous content
    for widget in parent.winfo_children():
        widget.destroy()

    # Create the main Tabview widget
    main_tabview = ctk.CTkTabview(parent)
    main_tabview.pack(pady=10, padx=10, fill="both", expand=True)

    # Add main tabs: Recording Tool and Control Tool
    recording_tool_tab = main_tabview.add("Recording Tool")
    control_tool_tab = main_tabview.add("Control Tool")
    validation_rules_tab = main_tabview.add("Validation Rules")
    validation_rules.create_validation_rules_tab(validation_rules_tab)

    # Add sub-tabs for Recording Tool
    recording_tool_sub_tabview = ctk.CTkTabview(recording_tool_tab)
    recording_tool_sub_tabview.pack(pady=10, padx=10, fill="both", expand=True)

    # Add "Algemeen" sub-tab
    tab_algemeen = recording_tool_sub_tabview.add("Algemeen")
    gui_algemeen.create_algemeen_tab(tab_algemeen, algemeen_data)


def FAKE_DATA_FUNC(url):
    """Simulate a long-running operation with a delay."""
    print(f"Fetching data for URL: {url}")
    time.sleep(2)  # Simulate delay (10 seconds)
    print("sleep for 2 seocnds to simulate crawl")
    return func.load_json("./data.json")

def handle_search(url_entry, display_frame):
    print("IN THE GUI")
    url = url_entry.get()
    print("url:", url)

    # Add a status label to indicate the fetching process
    status_label = ctk.CTkLabel(display_frame, text="Data is being fetched, please wait...", anchor="center")
    status_label.pack(pady=10)

    # Define the worker function to run in a separate thread
    def worker():
        # Replace `single_crawler` with `FAKE_DATA_FUNC` for testing
        data = FAKE_DATA_FUNC(url)
        
        # Update the UI after fetching the data
        def update_ui():
            # Update status label
            status_label.configure(text="Crawl complete!")
            # Display the fetched data
            display_data(data, display_frame)

        # Call update_ui on the main thread
        display_frame.after(0, update_ui)

    # Start the worker function in a new thread
    threading.Thread(target=worker, daemon=True).start()


# Separate function to add the Search tab
def add_search_tab(tabview):
    search_tab = tabview.add("Search")
    
    # Input field for URL
    url_label = ctk.CTkLabel(search_tab, text="Enter URL:", font=("Arial", 14))
    url_label.pack(pady=5)
    url_entry = ctk.CTkEntry(search_tab, placeholder_text="", width=300)  # Adjusted width for larger input field
    url_entry.pack(pady=5)

    # Button to trigger search
    search_button = ctk.CTkButton(search_tab, text="Search", command=lambda: handle_search(url_entry, display_frame))
    search_button.pack(pady=10)

    # Frame to display fetched data
    display_frame = ctk.CTkFrame(search_tab, width=500, height=300)
    display_frame.pack(pady=10, fill="both", expand=True)

# Modify the original add_admin_tab function to call the two new functions
def add_admin_tab(tabview):
    admin_tab = tabview.add("Admin")

    # Create a frame for Admin Controls
    admin_frame = ctk.CTkFrame(admin_tab)
    admin_frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Call the credentials_crud function
    gui_credenitals.credentials_crud(admin_frame)

# Function to open the main window with tabs based on user type
def open_main_window(root, is_admin):
    root.withdraw()  # Hide the login window
    main_window = ctk.CTkToplevel()
    
    # Maximize the main window to fill the screen
    main_window.geometry(f"{main_window.winfo_screenwidth()}x{main_window.winfo_screenheight()}")
    main_window.title("Main Page")

    # Create a Tabview widget that dynamically adjusts to the window size
    tabview = ctk.CTkTabview(main_window)
    tabview.pack(pady=0, padx=0, expand=True, fill="both")  # Remove padding for full coverage

    # Add tabs
    add_search_tab(tabview)  # Add the Search tab for all users
    if is_admin:
        add_admin_tab(tabview)  # Add the Admin tab only for admins



def main():
    credentials = crud_credentials.load_credentials()
    # print(credentials)

    # Initialize the main window
    # Initialize the main window
    root = ctk.CTk()
    root.title("Login Screen")
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")  # Set to full screen size


    
    
    if test_mode:
        hyperSel.colors_utilities.c_print("GUI TESTING MODE", "blue")
        # In test mode, skip login and open main window as admin
        open_main_window(root, is_admin=True)
    else:
        # Username label and entry
        username_label = ctk.CTkLabel(root, text="Username", font=("Arial", 16))
        username_label.pack(pady=20)
        username_entry = ctk.CTkEntry(root, width=300, font=("Arial", 16))
        username_entry.pack(pady=10)

        # Password label and entry
        password_label = ctk.CTkLabel(root, text="Password", font=("Arial", 16))
        password_label.pack(pady=20)
        password_entry = ctk.CTkEntry(root, show="*", width=300, font=("Arial", 16))
        password_entry.pack(pady=10)

        # Login button
        login_button = ctk.CTkButton(
            root,
            text="Login",
            command=lambda: validate_login(username_entry.get(), password_entry.get(), root, credentials),
            width=150,
            font=("Arial", 16)
        )
        login_button.pack(pady=40)

    
    # Run the application
    root.mainloop()


if __name__ == '__main__':
    main()
