import customtkinter as ctk
from tkinter import messagebox
import json

import hyperSel.colors_utilities
import hyperSel.selenium_utilities
import crud_credentials
import custom_log
import hyperSel
import validation_rules
import tkinter as tk
from tkinter import ttk
from difflib import SequenceMatcher
import customtkinter as ctk

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
# Function to display the fetched data in the search tab
def display_data(data, parent):
    # Clear any previous content
    for widget in parent.winfo_children():
        widget.destroy()

    # Display data in a scrollable text widget
    text_widget = ctk.CTkTextbox(parent, wrap="none", width=500, height=300)
    text_widget.insert("1.0", json.dumps(data, indent=4))  # Pretty print JSON
    text_widget.pack(pady=10, padx=10, fill="both", expand=True)


# Function to handle search button click
def handle_search(url_entry, display_frame):
    url = url_entry.get()
    if url:  # Simulate fetching data
        data = fake_fetch_data(url)
        display_data(data, display_frame)


# Separate function to add the Search tab
def add_search_tab(tabview):
    search_tab = tabview.add("Search")
    # Input field for URL
    url_label = ctk.CTkLabel(search_tab, text="Enter URL:", font=("Arial", 14))
    url_label.pack(pady=5)
    url_entry = ctk.CTkEntry(search_tab, placeholder_text="https://example.com")
    url_entry.pack(pady=5)

    # Button to trigger search
    search_button = ctk.CTkButton(search_tab, text="Search", command=lambda: handle_search(url_entry, display_frame))
    search_button.pack(pady=10)

    # Frame to display fetched data
    display_frame = ctk.CTkFrame(search_tab, width=500, height=300)
    display_frame.pack(pady=10, fill="both", expand=True)

def fake_fetch_data(url):
    print("url;", url)
    # Simulated JSON data
    data = custom_log.read_from_file("./logs/crawl_data.json")[0]
    return data

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

    # Call the validation_rules function
    validation_rules_framing(validation_rules_frame)

def validation_rules_framing(admin_frame):
    import custom_log

    # Load data
    data = custom_log.read_from_file("./logs/crawl_data.json")
    
    # Extract all unique questions
    all_questions = []
    for item in data:
        extracted_questions = validation_rules.extract_question_answer_pairs(item)
        for question in extracted_questions:
            if question['question'] not in all_questions:
                all_questions.append(question['question'])
    
    # Display a table-like layout
    for idx, question_text in enumerate(all_questions):
        # Display the question
        question_label = ctk.CTkLabel(admin_frame, text=question_text, font=("Arial", 12))
        question_label.grid(row=idx, column=0, pady=5, padx=10, sticky="w")
        
        # Add "Select" button
        select_button = ctk.CTkButton(
            admin_frame, text="Select", 
            command=lambda q=question_text: handle_question_selection(q, admin_frame)
        )
        select_button.grid(row=idx, column=1, pady=5, padx=10, sticky="e")


def handle_question_selection(question_text, admin_frame):
    # Clear the frame for the new selection
    for widget in admin_frame.winfo_children():
        widget.destroy()

    # Display the selected question
    question_label = ctk.CTkLabel(admin_frame, text=question_text, font=("Arial", 16))
    question_label.grid(row=0, column=0, pady=20, padx=10, sticky="w")

    # Add True/False buttons
    def submit_answer(value):
        print(f"Question: {question_text}, Answer: {value}")

    true_button = ctk.CTkButton(admin_frame, text="True", command=lambda: submit_answer(True))
    true_button.grid(row=1, column=0, pady=10, padx=10, sticky="w")

    false_button = ctk.CTkButton(admin_frame, text="False", command=lambda: submit_answer(False))
    false_button.grid(row=1, column=1, pady=10, padx=10, sticky="e")

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
    main_window.geometry("1200x800")
    main_window.title("Main Page")

    # Create a Tabview widget
    tabview = ctk.CTkTabview(main_window, width=700, height=700)
    tabview.pack(pady=20, padx=20, expand=True)

    # Add tabs
    add_search_tab(tabview)  # Add the Search tab for all users
    if is_admin:
        add_admin_tab(tabview)  # Add the Admin tab only for admins
    if is_admin:
        add_validation_rules_tab(tabview)  # Add the Admin tab only for admins

def main():
    credentials = crud_credentials.load_credentials()
    # print(credentials)

    # Initialize the main window
    root = ctk.CTk()
    root.geometry("1200x800")
    root.title("Login Screen")

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
