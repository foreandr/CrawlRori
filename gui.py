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

# Test mode flag to skip login
test_mode = True

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

    # Clear any previous content
    for widget in parent.winfo_children():
        widget.destroy()

    # Create the main Tabview widget
    main_tabview = ctk.CTkTabview(parent)
    main_tabview.pack(pady=10, padx=10, fill="both", expand=True)

    # Add main tabs: Recording Tool and Control Tool
    recording_tool_tab = main_tabview.add("Recording Tool")
    control_tool_tab = main_tabview.add("Control Tool")

    # Add sub-tabs for Recording Tool
    recording_tool_sub_tabview = ctk.CTkTabview(recording_tool_tab)
    recording_tool_sub_tabview.pack(pady=10, padx=10, fill="both", expand=True)

    tab_algemeen = recording_tool_sub_tabview.add("Algemeen")  # General
    tab_omgevingskenmerken = recording_tool_sub_tabview.add("Omgevingskenmerken")  # Environmental Features
    tab_gebouwen = recording_tool_sub_tabview.add("Gebouwen")  # Buildings
    tab_ruimtes = recording_tool_sub_tabview.add("Ruimtes")  # Spaces
    tab_schades = recording_tool_sub_tabview.add("Schades")  # Damages
    tab_bijlagen = recording_tool_sub_tabview.add("Bijlagen")  # Attachments
    tab_samenvatting = recording_tool_sub_tabview.add("Samenvatting")  # Summary

    # Add content to each sub-tab for Recording Tool
    label_algemeen = ctk.CTkLabel(tab_algemeen, text="Content for Algemeen")
    label_algemeen.pack(pady=20)

    label_omgevingskenmerken = ctk.CTkLabel(tab_omgevingskenmerken, text="Content for Omgevingskenmerken")
    label_omgevingskenmerken.pack(pady=20)

    label_gebouwen = ctk.CTkLabel(tab_gebouwen, text="Content for Gebouwen")
    label_gebouwen.pack(pady=20)

    label_ruimtes = ctk.CTkLabel(tab_ruimtes, text="Content for Ruimtes")
    label_ruimtes.pack(pady=20)

    label_schades = ctk.CTkLabel(tab_schades, text="Content for Schades")
    label_schades.pack(pady=20)

    label_bijlagen = ctk.CTkLabel(tab_bijlagen, text="Content for Bijlagen")
    label_bijlagen.pack(pady=20)

    label_samenvatting = ctk.CTkLabel(tab_samenvatting, text="Content for Samenvatting")
    label_samenvatting.pack(pady=20)

    # Add sub-tabs for Control Tool
    control_tool_sub_tabview = ctk.CTkTabview(control_tool_tab)
    control_tool_sub_tabview.pack(pady=10, padx=10, fill="both", expand=True)

    tab_informatie = control_tool_sub_tabview.add("Informatie")  # Information
    tab_calculatie = control_tool_sub_tabview.add("Calculatie")  # Calculation

    # Add content to each sub-tab for Control Tool
    label_informatie = ctk.CTkLabel(tab_informatie, text="Content for Informatie")
    label_informatie.pack(pady=20)

    label_calculatie = ctk.CTkLabel(tab_calculatie, text="Content for Calculatie")
    label_calculatie.pack(pady=20)

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

def credentials_crud(admin_frame):
    credentials_label = ctk.CTkLabel(admin_frame, text="Credentials Management", font=("Arial", 16))
    credentials_label.grid(row=0, column=0, pady=10, padx=10, sticky="w")

    # Frame to contain account rows for easy clearing and reloading
    rows_frame = ctk.CTkFrame(admin_frame)
    rows_frame.grid(row=1, column=0, columnspan=6, sticky="nsew")

    # Function to load and display account rows
    def load_account_rows():
        # Clear existing rows including the '+' button if present
        for widget in rows_frame.winfo_children():
            widget.destroy()

        credentials = crud_credentials.load_credentials()
        row_counter = 1

        # Create rows for admin and user accounts
        for account in credentials["admin_accounts"]:
            create_account_row(rows_frame, row_counter, "admin", account)
            row_counter += 1

        for account in credentials["user_accounts"]:
            create_account_row(rows_frame, row_counter, "user", account)
            row_counter += 1

        # Add button to create a new row at the end (outside the loop to avoid duplication)
        add_button = ctk.CTkButton(rows_frame, text="+", font=("Arial", 16), command=add_new_account_row)
        add_button.grid(row=row_counter + 1, column=0, pady=10, padx=10, sticky="w")

    # Function to display account info with delete button
    def create_account_row(frame, row, account_type, account_data):
        # Editable Username and Password fields
        username_label = ctk.CTkLabel(frame, text="Username", font=("Arial", 12))
        username_label.grid(row=row, column=0, pady=5, padx=10, sticky="w")
        username_input = ctk.CTkEntry(frame, font=("Arial", 12))
        username_input.insert(0, account_data["username"])
        username_input.grid(row=row, column=1, pady=5, padx=10, sticky="w")

        password_label = ctk.CTkLabel(frame, text="Password", font=("Arial", 12))
        password_label.grid(row=row, column=2, pady=5, padx=10, sticky="w")
        password_input = ctk.CTkEntry(frame, font=("Arial", 12), show="*")
        password_input.insert(0, account_data["password"])
        password_input.grid(row=row, column=3, pady=5, padx=10, sticky="w")

        # Admin Checkbox
        is_admin = True if account_type == "admin" else False
        admin_checkbox = ctk.CTkCheckBox(frame, text="Admin", variable=ctk.BooleanVar(value=is_admin), font=("Arial", 12), state="disabled")
        admin_checkbox.grid(row=row, column=4, pady=5, padx=10, sticky="w")

        # Delete Button (calls delete_account function and refreshes rows)
        delete_button = ctk.CTkButton(frame, text="Delete", font=("Arial", 12),
                                      command=lambda: (crud_credentials.delete_account(account_type, username_input.get()), load_account_rows()))
        delete_button.grid(row=row, column=5, pady=5, padx=10)

    # Function to add a new row for creating a new account
    def add_new_account_row():
        new_row = rows_frame.grid_size()[1] + 1
        username_input = ctk.CTkEntry(rows_frame, font=("Arial", 12))
        username_input.grid(row=new_row, column=1, pady=5, padx=10, sticky="w")

        password_input = ctk.CTkEntry(rows_frame, font=("Arial", 12), show="*")
        password_input.grid(row=new_row, column=3, pady=5, padx=10, sticky="w")

        admin_checkbox = ctk.CTkCheckBox(rows_frame, text="Admin", font=("Arial", 12))
        admin_checkbox.grid(row=new_row, column=4, pady=5, padx=10, sticky="w")

        # Save Button (creates new account and reloads rows)
        save_button = ctk.CTkButton(rows_frame, text="Save", font=("Arial", 12),
                                     command=lambda: (crud_credentials.create_account(
                                         "admin" if admin_checkbox.get() else "user",
                                         username_input.get(), password_input.get()), load_account_rows()))
        save_button.grid(row=new_row, column=5, pady=5, padx=10)

    # Initial load of account rows
    load_account_rows()


# Add a new credential inline (no new window, just a new row)
def add_new_account(row_counter, admin_frame):
    # Add input fields for new credential
    username_label = ctk.CTkLabel(admin_frame, text="Username", font=("Arial", 12))
    username_label.grid(row=row_counter, column=0, pady=5, padx=10, sticky="w")
    username_input = ctk.CTkEntry(admin_frame, font=("Arial", 12))
    username_input.grid(row=row_counter, column=1, pady=5, padx=10, sticky="w")

    password_label = ctk.CTkLabel(admin_frame, text="Password", font=("Arial", 12))
    password_label.grid(row=row_counter, column=2, pady=5, padx=10, sticky="w")
    password_input = ctk.CTkEntry(admin_frame, font=("Arial", 12), show="*")
    password_input.grid(row=row_counter, column=3, pady=5, padx=10, sticky="w")

    is_admin_var = ctk.StringVar(value="no")
    admin_checkbox = ctk.CTkCheckBox(admin_frame, text="Admin", variable=is_admin_var, font=("Arial", 12))
    admin_checkbox.grid(row=row_counter, column=4, pady=5, padx=10, sticky="w")

    save_button = ctk.CTkButton(admin_frame, text="Save", font=("Arial", 12), command=lambda: save_new_account(username_input.get(), password_input.get(), is_admin_var.get()))
    save_button.grid(row=row_counter, column=5, pady=5, padx=10)

# Save the new account
def save_new_account(username, password, is_admin):
    credentials = crud_credentials.load_credentials()
    
    # Add the new account to the correct list based on admin checkbox
    account_type = "admin" if is_admin == "yes" else "user"
    
    # Check if username already exists
    if any(account["username"] == username for account in credentials[account_type + "_accounts"]):
        # print("Username already exists.")
        return

    credentials[account_type + "_accounts"].append({"username": username, "password": password})
    crud_credentials.save_credentials(credentials)
    # print(f"{account_type.capitalize()} account created successfully.")

def add_validation_rules_tab(tabview):
    validation_rules_tab = tabview.add("Validation Rules")

    # Create a frame for Admin Controls
    validation_rules_frame = ctk.CTkFrame(validation_rules_tab)
    validation_rules_frame.pack(pady=20, padx=20, fill="both", expand=True)


# Modify the original add_admin_tab function to call the two new functions
def add_admin_tab(tabview):
    admin_tab = tabview.add("Admin")

    # Create a frame for Admin Controls
    admin_frame = ctk.CTkFrame(admin_tab)
    admin_frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Call the credentials_crud function
    credentials_crud(admin_frame)

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
    if is_admin:
        add_validation_rules_tab(tabview)  # Add the Validation Rules tab only for admins


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
