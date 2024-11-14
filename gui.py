import customtkinter as ctk
from tkinter import messagebox
import json
import crud_credentials

# Test mode flag to skip login
test_mode = False

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
def add_search_tab(tabview):
    search_tab = tabview.add("Search")
    search_label = ctk.CTkLabel(search_tab, text="Search Functionality Here", font=("Arial", 16))
    search_label.pack(pady=20)
    # Additional search functionality can go here

# Separate function to add the Admin tab
def add_admin_tab(tabview):
    admin_tab = tabview.add("Admin")
    admin_label = ctk.CTkLabel(admin_tab, text="Admin Controls Here", font=("Arial", 16))
    admin_label.pack(pady=20)
    # Additional admin functionality can go here

# Function to open the main window with tabs based on user type
def open_main_window(root, is_admin):
    root.withdraw()  # Hide the login window
    main_window = ctk.CTkToplevel()
    main_window.geometry("800x800")
    main_window.title("Main Page")

    # Create a Tabview widget
    tabview = ctk.CTkTabview(main_window, width=700, height=700)
    tabview.pack(pady=20, padx=20, expand=True)

    # Add tabs
    add_search_tab(tabview)  # Add the Search tab for all users
    if is_admin:
        add_admin_tab(tabview)  # Add the Admin tab only for admins

def main():
    credentials = crud_credentials.load_credentials()
    print(credentials)

    # Initialize the main window
    root = ctk.CTk()
    root.geometry("800x800")
    root.title("Login Screen")

    if test_mode:
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
