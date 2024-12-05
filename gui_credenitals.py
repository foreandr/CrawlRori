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