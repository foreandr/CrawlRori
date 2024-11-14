import json
# Define accounts with separate admin and user accounts
default_account = {
    "admin_accounts": [
        {"username": "admin1", "password": "password"},
        {"username": "admin2", "password": "password"},
    ],
    "user_accounts": [
        {"username": "user1", "password": "password"},
        {"username": "user2", "password": "password"},
    ],
}


# Main application setup
# Save credentials to credentials.json
def save_credentials(data):
    with open("credentials.json", "w") as file:
        json.dump(data, file, indent=4)
    print("Credentials saved to credentials.json")

def load_credentials():
    try:
        with open("credentials.json", "r") as file:
            credentials = json.load(file)
        print("Credentials loaded successfully")
        return credentials
    except FileNotFoundError:
        # If file is missing, create it with default_account data
        print("credentials.json not found. Creating with default accounts.")
        save_credentials(default_account)
        return load_credentials()  # Load newly created file

# Create a new account, checking for duplicate usernames
def create_account(account_type, username, password):
    credentials = load_credentials()
    accounts = credentials[account_type + "_accounts"]
    
    # Check for duplicates
    if any(account["username"] == username for account in accounts):
        print("Username already exists.")
        return

    accounts.append({"username": username, "password": password})
    save_credentials(credentials)
    print(f"{account_type.capitalize()} account created successfully.")

# Read all accounts (print loaded credentials)
def print_credentials():
    credentials = load_credentials()
    print("Loaded Credentials:", credentials)

# Update an existing account
def update_account(account_type, username, new_password):
    credentials = load_credentials()
    accounts = credentials[account_type + "_accounts"]

    for account in accounts:
        if account["username"] == username:
            account["password"] = new_password
            save_credentials(credentials)
            print(f"{account_type.capitalize()} account updated successfully.")
            return

    print("Username not found.")

# Delete an account
def delete_account(account_type, username):
    credentials = load_credentials()
    accounts = credentials[account_type + "_accounts"]

    for i, account in enumerate(accounts):
        if account["username"] == username:
            del accounts[i]
            save_credentials(credentials)
            print(f"{account_type.capitalize()} account deleted successfully.")
            return

    print("Username not found.")