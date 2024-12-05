import customtkinter as ctk
from tkinter import messagebox
import json
import os
import gui
import validation_rules

VALIDATION_RULES_FILE = "./validation_rules.json"
VALIDATION_RESULTS_FILE = "./validation_results.csv"

my_validation_rules = []
demo_validation_rules = [
    {"type": "if", "answer": "Particulier", "condition": True, "location": "algemeen"},
    {"type": "then", "answer": "Gedeeltelijk particulier en gedeeltelijk zakelijk", "condition": True, "location": "algemeen"}
]


def create_validation_rules_tab(validation_rules_tab):
    """
    Creates the Validation Rules tab with two sub-tabs:
    - Create Validation Rules
    - Check Validation Rules
    """
    # Create the main TabView for the two sub-tabs
    sub_tabview = ctk.CTkTabview(validation_rules_tab)
    sub_tabview.pack(fill="both", expand=True, padx=10, pady=10)

    # Add "Create Validation Rules" tab
    create_tab = sub_tabview.add("Create Validation Rules")
    create_validation_tab(create_tab)

    # Add "Check Validation Rules" tab
    check_tab = sub_tabview.add("Check Validation Rules")
    create_check_validation_tab(check_tab)


def create_validation_tab(create_tab):
    global my_validation_rules
    """
    Creates the tab for creating validation rules with two panels:
    - Left Panel: If Rules
    - Right Panel: Then Rules
    """
    create_tab.grid_rowconfigure(0, weight=1)
    create_tab.grid_columnconfigure(0, weight=1)
    create_tab.grid_columnconfigure(1, weight=1)

    left_panel = ctk.CTkFrame(create_tab, corner_radius=10)
    left_panel.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    right_panel = ctk.CTkFrame(create_tab, corner_radius=10)
    right_panel.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    left_label = ctk.CTkLabel(left_panel, text="IF RULES", font=("Arial", 16, "bold"))
    left_label.pack(pady=10)

    right_label = ctk.CTkLabel(right_panel, text="THEN RULES", font=("Arial", 16, "bold"))
    right_label.pack(pady=10)

    def refresh_rules():
        for widget in left_panel.winfo_children():
            if widget != left_label:
                widget.destroy()

        for widget in right_panel.winfo_children():
            if widget != right_label:
                widget.destroy()

        for rule in my_validation_rules:
            if rule["type"] == "if":
                rule_text = f"{rule['location'].upper()} - {rule['answer']}: {'True' if rule['condition'] else 'False'}"
                rule_frame = ctk.CTkFrame(left_panel, corner_radius=8)
                rule_frame.pack(fill="x", pady=5, padx=10)

                rule_label = ctk.CTkLabel(rule_frame, text=rule_text, anchor="w", wraplength=300)
                rule_label.pack(fill="x", pady=5, padx=5)

        for rule in my_validation_rules:
            if rule["type"] == "then":
                rule_text = f"{rule['location'].upper()} - {rule['answer']}: {'True' if rule['condition'] else 'False'}"
                rule_frame = ctk.CTkFrame(right_panel, corner_radius=8)
                rule_frame.pack(fill="x", pady=5, padx=10)

                rule_label = ctk.CTkLabel(rule_frame, text=rule_text, anchor="w", wraplength=300)
                rule_label.pack(fill="x", pady=5, padx=5)

    def save_rules():
        if not os.path.exists(VALIDATION_RULES_FILE):
            with open(VALIDATION_RULES_FILE, "w") as file:
                json.dump([], file)

        with open(VALIDATION_RULES_FILE, "r") as file:
            all_rules = json.load(file)

        all_rules.append(my_validation_rules)

        with open(VALIDATION_RULES_FILE, "w") as file:
            json.dump(all_rules, file, indent=4)

        print(f"Rules successfully saved to {VALIDATION_RULES_FILE}")

    button_frame = ctk.CTkFrame(create_tab)
    button_frame.grid(row=1, column=0, columnspan=2, pady=10)

    refresh_button = ctk.CTkButton(button_frame, text="Refresh Rules", command=refresh_rules, width=120)
    refresh_button.pack(side="left", padx=10)

    save_button = ctk.CTkButton(button_frame, text="Save Rules", command=save_rules, width=120)
    save_button.pack(side="left", padx=10)

    refresh_rules()


def create_check_validation_tab(check_tab):
    """
    Creates the tab for checking validation rules against current data.
    """
    ITEMS_PER_PAGE = 2  # Items to display per page
    current_page = 0
    rules_to_display = []

    def load_rules():
        """Load rules from file and add demo rules."""
        nonlocal rules_to_display
        rules_to_display = []
        if os.path.exists(VALIDATION_RULES_FILE):
            with open(VALIDATION_RULES_FILE, "r") as file:
                rules_to_display = json.load(file)
        rules_to_display.append(demo_validation_rules)

    def display_rules():
        """Display rules for the current page."""
        nonlocal current_page
        for widget in left_display_frame.winfo_children():
            widget.destroy()

        start_idx = current_page * ITEMS_PER_PAGE
        end_idx = start_idx + ITEMS_PER_PAGE
        current_rules = rules_to_display[start_idx:end_idx]

        for idx, rule_set in enumerate(current_rules):
            rule_set_frame = ctk.CTkFrame(left_display_frame, corner_radius=8, border_width=1)
            rule_set_frame.pack(fill="x", pady=5, padx=10)

            for rule in rule_set:
                rule_text = f"{rule['location'].upper()} - {rule['type'].upper()}: {rule['answer']} = {'True' if rule['condition'] else 'False'}"
                rule_label = ctk.CTkLabel(rule_set_frame, text=rule_text, anchor="w", wraplength=600, font=("Arial", 12))
                rule_label.pack(fill="x", pady=2, padx=5)

            def check_rules(selected_rule_set=rule_set):
                print("Waiting for data...")

                # Load the current data from the file
                current_data = gui.load_current_data()

                print("Selected Rule Set:", selected_rule_set)
                print("Current Data Length:", len(current_data) if current_data else "No Data Available")

            def delete_rules(selected_index=start_idx + idx):
                if os.path.exists(VALIDATION_RULES_FILE):
                    with open(VALIDATION_RULES_FILE, "r") as file:
                        all_rules = json.load(file)

                    if selected_index < len(all_rules):
                        all_rules.pop(selected_index)
                        with open(VALIDATION_RULES_FILE, "w") as file:
                            json.dump(all_rules, file, indent=4)

                        print(f"Deleted Rule Set {selected_index + 1}")
                        load_rules()
                        display_rules()

            button_frame = ctk.CTkFrame(rule_set_frame)
            button_frame.pack(fill="x", pady=5, padx=5)

            ctk.CTkButton(
                button_frame, text="Check", command=check_rules, width=100, height=30
            ).pack(side="left", padx=5)

            ctk.CTkButton(
                button_frame,
                text="Delete",
                command=lambda i=idx: delete_rules(),
                fg_color="red",
                width=100,
                height=30,
            ).pack(side="left", padx=5)

        update_pagination_controls()

    def update_pagination_controls():
        """Update pagination buttons."""
        for widget in pagination_frame.winfo_children():
            widget.destroy()

        total_pages = (len(rules_to_display) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

        if current_page > 0:
            ctk.CTkButton(
                pagination_frame, text="Previous", command=lambda: go_to_page(current_page - 1), width=80, height=30
            ).pack(side="left", padx=5)

        ctk.CTkLabel(
            pagination_frame, text=f"Page {current_page + 1} of {total_pages}", font=("Arial", 12)
        ).pack(side="left", padx=5)

        if current_page < total_pages - 1:
            ctk.CTkButton(
                pagination_frame, text="Next", command=lambda: go_to_page(current_page + 1), width=80, height=30
            ).pack(side="left", padx=5)

    def go_to_page(page_index):
        """Navigate to a specific page."""
        nonlocal current_page
        current_page = page_index
        display_rules()

    def refresh_rules():
        """Reload and display the rules."""
        load_rules()
        display_rules()

    # Main split for left and right sections
    main_split_frame = ctk.CTkFrame(check_tab, corner_radius=10)
    main_split_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Left-hand side: List of rules with pagination
    left_display_frame = ctk.CTkFrame(main_split_frame)
    left_display_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

    # Right-hand side: Independent unified section
    right_display_frame = ctk.CTkFrame(main_split_frame, fg_color="lightgray")
    right_display_frame.pack(side="left", fill="both", expand=True)

    # Add "Hello World" to the right-hand side
    hello_label = ctk.CTkLabel(right_display_frame, text="Hello World", font=("Arial", 18, "bold"), anchor="center")
    hello_label.pack(fill="both", expand=True, pady=10, padx=10)

    # Pagination controls (only for the left-hand side)
    pagination_frame = ctk.CTkFrame(check_tab)
    pagination_frame.pack(fill="x", pady=5)

    # Bottom buttons: Refresh and Save
    bottom_frame = ctk.CTkFrame(check_tab)
    bottom_frame.pack(fill="x", pady=5)

    ctk.CTkButton(
        bottom_frame, text="Refresh Rules", command=refresh_rules, width=100, height=30
    ).pack(side="left", padx=10)

    ctk.CTkButton(
        bottom_frame, text="Save Results to CSV", command=lambda: print(f"Saving to {VALIDATION_RESULTS_FILE}"), width=150, height=30
    ).pack(side="left", padx=10)

    # Refresh and load rules
    refresh_rules()