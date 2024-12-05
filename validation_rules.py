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
import os
import json

import gui_credenitals
VALIDATION_RULES_FILE = "./validation_rules.json"
my_validation_rules = []
demo_validation_rules = [
    {"type": "if","answer": "Particulier","condition": True,"location": "algemeen"},
    {"type": "then","answer": "Gedeeltelijk particulier en gedeeltelijk zakelijk","condition": True, "location": "algemeen"}
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

    # Create a grid layout for the tab
    create_tab.grid_rowconfigure(0, weight=1)
    create_tab.grid_columnconfigure(0, weight=1)  # Left panel
    create_tab.grid_columnconfigure(1, weight=1)  # Right panel

    # Create Left Panel for If Rules
    left_panel = ctk.CTkFrame(create_tab, corner_radius=10)
    left_panel.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # Create Right Panel for Then Rules
    right_panel = ctk.CTkFrame(create_tab, corner_radius=10)
    right_panel.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    # Add labels for panel headers
    left_label = ctk.CTkLabel(left_panel, text="IF RULES", font=("Arial", 16, "bold"))
    left_label.pack(pady=10)

    right_label = ctk.CTkLabel(right_panel, text="THEN RULES", font=("Arial", 16, "bold"))
    right_label.pack(pady=10)

    def refresh_rules():
        """Refreshes the displayed validation rules in both panels."""
        # Clear content in both panels
        for widget in left_panel.winfo_children():
            if widget != left_label:  # Skip the header label
                widget.destroy()

        for widget in right_panel.winfo_children():
            if widget != right_label:  # Skip the header label
                widget.destroy()

        # Populate If Rules in the left panel
        for rule in my_validation_rules:
            if rule["type"] == "if":
                rule_text = f"{rule['location'].upper()} - {rule['answer']}: {'True' if rule['condition'] else 'False'}"
                rule_frame = ctk.CTkFrame(left_panel, corner_radius=8)
                rule_frame.pack(fill="x", pady=5, padx=10)

                rule_label = ctk.CTkLabel(rule_frame, text=rule_text, anchor="w", wraplength=300)
                rule_label.pack(fill="x", pady=5, padx=5)

        # Populate Then Rules in the right panel
        for rule in my_validation_rules:
            if rule["type"] == "then":
                rule_text = f"{rule['location'].upper()} - {rule['answer']}: {'True' if rule['condition'] else 'False'}"
                rule_frame = ctk.CTkFrame(right_panel, corner_radius=8)
                rule_frame.pack(fill="x", pady=5, padx=10)

                rule_label = ctk.CTkLabel(rule_frame, text=rule_text, anchor="w", wraplength=300)
                rule_label.pack(fill="x", pady=5, padx=5)

    def save_rules():
        """Saves the current rules to a single JSON file, appending to the existing list of rule sets."""
        # Check if the file exists, and create it if not
        if not os.path.exists(VALIDATION_RULES_FILE):
            with open(VALIDATION_RULES_FILE, "w") as file:
                json.dump([], file)  # Initialize the file with an empty list

        # Load existing rules from the file
        with open(VALIDATION_RULES_FILE, "r") as file:
            all_rules = json.load(file)

        # Append the current set of rules to the list
        all_rules.append(my_validation_rules)

        # Save back to the file
        with open(VALIDATION_RULES_FILE, "w") as file:
            json.dump(all_rules, file, indent=4)

        print(f"Rules successfully saved to {VALIDATION_RULES_FILE}")

    # Add a frame at the bottom for the buttons
    button_frame = ctk.CTkFrame(create_tab)
    button_frame.grid(row=1, column=0, columnspan=2, pady=10)

    # Add the Refresh Rules button
    refresh_button = ctk.CTkButton(
        button_frame,
        text="Refresh Rules",
        command=refresh_rules,
        width=120,
    )
    refresh_button.pack(side="left", padx=10)

    # Add the Save Rules button
    save_button = ctk.CTkButton(
        button_frame,
        text="Save Rules",
        command=save_rules,
        width=120,
    )
    save_button.pack(side="left", padx=10)

    # Initial display of rules
    refresh_rules()

def create_check_validation_tab(check_tab):
    """
    Creates the tab for checking validation rules against current data.
    """
    check_tab.grid_rowconfigure(0, weight=1)
    check_tab.grid_columnconfigure(0, weight=1)

    # Add a label for instructions
    instruction_label = ctk.CTkLabel(
        check_tab, text="Loaded Validation Rules:", font=("Arial", 14, "bold"), anchor="w"
    )
    instruction_label.pack(pady=10, padx=10)

    # Frame to display validation rules
    rules_display_frame = ctk.CTkFrame(check_tab, corner_radius=10)
    rules_display_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def display_rules():
        """Load and display rules in the frame."""
        # Clear existing content
        for widget in rules_display_frame.winfo_children():
            widget.destroy()

        # Load rules from file and include demo rules
        rules_to_display = []
        if os.path.exists(VALIDATION_RULES_FILE):
            with open(VALIDATION_RULES_FILE, "r") as file:
                rules_to_display = json.load(file)

        # Add demo rules
        rules_to_display.append(demo_validation_rules)

        # Display each rule set
        for rule_set in rules_to_display:
            rule_set_frame = ctk.CTkFrame(rules_display_frame, corner_radius=8, border_width=1)
            rule_set_frame.pack(fill="x", pady=5, padx=10)

            for rule in rule_set:
                rule_text = f"{rule['location'].upper()} - {rule['type'].upper()}: {rule['answer']} = {'True' if rule['condition'] else 'False'}"
                rule_label = ctk.CTkLabel(
                    rule_set_frame, text=rule_text, anchor="w", wraplength=600, font=("Arial", 12)
                )
                rule_label.pack(fill="x", pady=2, padx=5)

    # Display rules on tab load
    display_rules()

    # Add a refresh button to reload rules
    refresh_button = ctk.CTkButton(
        check_tab, text="Refresh Rules", command=display_rules, width=120
    )
    refresh_button.pack(pady=10)
