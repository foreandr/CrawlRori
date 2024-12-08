import customtkinter as ctk
from tkinter import messagebox
import json
import os

import hyperSel.colors_utilities
import gui
import validation_rules
import hyperSel
import validation_logic

VALIDATION_RULES_FILE = "./validation_rules.json"
VALIDATION_RESULTS_FILE = "./validation_results.csv"

my_validation_rules = []
demo_validation_rules = [
    {
        "type": "if",
        "question": "Welke situatie is van toepassing? De aanvrager is (DEMO RULE, CANT BE DELETED):",
        "answer": "Particulier",
        "condition": True,
        "location": "algemeen",
    },
    {
        "type": "then",
        "question": "Welke situatie is van toepassing? De aanvrager is:",
        "answer": "Zakelijk",
        "condition": True,
        "location": "algemeen",
    },
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
    """
    Creates the tab for creating validation rules with two panels:
    - Left Panel: If Rules
    - Right Panel: Then Rules
    """
    global my_validation_rules

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
            # print("rule:", rule)

            rule_text = (
                f"{rule['location'].upper()} - {rule['question']}\n"
                f"Answer: {rule['answer']} - Condition: {'True' if rule['condition'] else 'False'}"
            )

            if rule["type"] == "if":
                rule_frame = ctk.CTkFrame(left_panel, corner_radius=8)
                rule_frame.pack(fill="x", pady=5, padx=10)

                rule_label = ctk.CTkLabel(rule_frame, text=rule_text, anchor="w", wraplength=300)
                rule_label.pack(fill="x", pady=5, padx=5)

            if rule["type"] == "then":
                rule_frame = ctk.CTkFrame(right_panel, corner_radius=8)
                rule_frame.pack(fill="x", pady=5, padx=10)

                rule_label = ctk.CTkLabel(rule_frame, text=rule_text, anchor="w", wraplength=300)
                rule_label.pack(fill="x", pady=5, padx=5)

    def save_rules():
        if not os.path.exists(VALIDATION_RULES_FILE):
            # Create the file and initialize it as an empty list
            with open(VALIDATION_RULES_FILE, "w") as file:
                json.dump([], file)

        try:
            # Open the file and load its content
            with open(VALIDATION_RULES_FILE, "r") as file:
                content = file.read()
                all_rules = json.loads(content) if content.strip() else []
        except json.JSONDecodeError:
            # If the file content is invalid, reset to an empty list
            all_rules = []

        # Append the new set of rules (as a list) to the main list
        all_rules.append(my_validation_rules)

        # Save back to the file
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

        # Ensure the file exists and is initialized as an empty list if missing
        if not os.path.exists(VALIDATION_RULES_FILE):
            with open(VALIDATION_RULES_FILE, "w") as file:
                json.dump([], file)

        # Read the file, handling empty or invalid content gracefully
        with open(VALIDATION_RULES_FILE, "r") as file:
            try:
                rules_to_display = json.load(file)
                if not isinstance(rules_to_display, list):
                    raise ValueError("Rules file must contain a list")
            except (json.JSONDecodeError, ValueError):
                rules_to_display = []

        # Add demo rules to the display
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
            # Create a frame for each rule set
            rule_set_frame = ctk.CTkFrame(left_display_frame, corner_radius=8, border_width=1)
            rule_set_frame.pack(fill="x", pady=5, padx=10)

            # Display each rule within the rule set
            for rule in rule_set:
                rule_text = (
                    f"{rule['location'].upper()} - {rule['type'].upper()}\n"
                    f"Question: {rule['question']}\n"
                    f"Answer: {rule['answer']} - Condition: {'✔️' if rule['condition'] else '❌'}"
                )
                rule_label = ctk.CTkLabel(
                    rule_set_frame,
                    text=rule_text,
                    anchor="w",
                    wraplength=600,
                    font=("Arial", 12),
                    justify="left",  # Align text to the left for a clean layout
                )
                rule_label.pack(fill="x", pady=(5, 10), padx=5)  # Add spacing between rules

            # Create a frame for buttons
            button_frame = ctk.CTkFrame(rule_set_frame)
            button_frame.pack(fill="x", pady=5, padx=5)

            # Check button
            ctk.CTkButton(
                button_frame,
                text="Check",
                command=lambda rs=rule_set: check_rules(rs),
                width=100,
                height=30,
            ).pack(side="left", padx=5)

            # Delete button
            ctk.CTkButton(
                button_frame,
                text="Delete",
                command=lambda i=start_idx + idx: delete_rules(i),
                fg_color="red",
                width=100,
                height=30,
            ).pack(side="right", padx=5)

        # Update pagination controls at the bottom
        update_pagination_controls()

    def check_rules(selected_rule_set):
        """
        Handles the functionality of the 'Check' button to validate rules
        against the current data.
        """
        # print("Waiting for data...")

        # Load the current data from the file
        current_data = gui.load_current_data()

        # Perform validation and update the validation section
        update_validation_section(current_data, selected_rule_set)

    def delete_rules(selected_index):
        """
        Handles the functionality of the 'Delete' button to remove a rule
        set from the validation rules file.
        """
        if os.path.exists(VALIDATION_RULES_FILE):
            with open(VALIDATION_RULES_FILE, "r") as file:
                all_rules = json.load(file)

            # Check if the selected index is valid before attempting deletion
            if selected_index < len(all_rules):
                all_rules.pop(selected_index)
                with open(VALIDATION_RULES_FILE, "w") as file:
                    json.dump(all_rules, file, indent=4)

                print(f"Deleted Rule Set {selected_index + 1}")

                # Reload and redisplay rules after deletion
                load_rules()
                display_rules()
                
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

    # Top Section: Pagination and Buttons
    top_section = ctk.CTkFrame(check_tab)
    top_section.pack(fill="x", pady=5)

    # Pagination controls on the left
    pagination_frame = ctk.CTkFrame(top_section)
    pagination_frame.pack(side="left", padx=10)

    # Save and Refresh buttons on the right
    button_frame = ctk.CTkFrame(top_section)
    button_frame.pack(side="right", padx=10)

    ctk.CTkButton(
        button_frame, text="Refresh Rules", command=refresh_rules, width=100, height=30
    ).pack(side="left", padx=10)

    ctk.CTkButton(
        button_frame, text="Save Results to CSV", command=lambda: print(f"Saving to {VALIDATION_RESULTS_FILE}"), width=150, height=30
    ).pack(side="left", padx=10)

    # Main split for left and right sections
    main_split_frame = ctk.CTkFrame(check_tab, corner_radius=10)
    main_split_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Left-hand side: List of rules with pagination
    left_display_frame = ctk.CTkFrame(main_split_frame)
    left_display_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

    # Right-hand side: Independent unified section
    update_validation_section = create_validation_data_section(main_split_frame)

    # Initialize the rules and controls
    refresh_rules()

def create_validation_data_section(parent_frame):
    """
    Creates the Validation Section on the right-hand side.
    Splits the section into a green side for successes and a red side for failures.
    """
    validation_data_frame = ctk.CTkFrame(parent_frame)
    validation_data_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

    title_label = ctk.CTkLabel(validation_data_frame, text="Validation Section", font=("Arial", 20, "bold"))
    title_label.pack(pady=10)

    # Success Frame (Green Side)
    success_frame = ctk.CTkFrame(validation_data_frame, corner_radius=10, border_width=2, border_color="green")
    success_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    success_title_label = ctk.CTkLabel(success_frame, text="Validation Successes", font=("Arial", 16, "bold"), text_color="green")
    success_title_label.pack(pady=5, padx=10)

    success_textbox = ctk.CTkTextbox(success_frame, wrap="word", font=("Arial", 12), fg_color="#111", text_color="#d4edda", border_color="#28a745", corner_radius=5)
    success_textbox.pack(fill="both", expand=True, padx=10, pady=10)
    success_textbox.configure(state="disabled")  # Make it read-only by default

    # Failures Frame (Red Side)
    failures_frame = ctk.CTkFrame(validation_data_frame, corner_radius=10, border_width=2, border_color="red")
    failures_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    failures_title_label = ctk.CTkLabel(failures_frame, text="Validation Failures", font=("Arial", 16, "bold"), text_color="red")
    failures_title_label.pack(pady=5, padx=10)

    failures_textbox = ctk.CTkTextbox(failures_frame, wrap="word", font=("Arial", 12), fg_color="#111", text_color="#f8d7da", border_color="#dc3545", corner_radius=5)
    failures_textbox.pack(fill="both", expand=True, padx=10, pady=10)
    failures_textbox.configure(state="disabled")  # Make it read-only by default

    def update_validation_section(current_data, selected_rule_set):
        """
        Updates the Validation Section with new validation results.
        """
        final_rule_dict = validation_logic.validation_rule_tool(
            current_data=current_data, selected_rule_set=selected_rule_set
        )

        # Update Successes Textbox
        success_textbox.configure(state="normal")  # Enable editing
        success_textbox.delete("1.0", "end")  # Clear existing content

        # Confirmed IF Rules (Displayed Before THEN Rules)
        if_successes = final_rule_dict.get("all_if_rules_confirmed", [])
        if if_successes:
            success_textbox.insert("end", "CONFIRMED IF RULES:\n", "bold_green")
            success_textbox.insert("end", "===============\n", "bold_green")
            for idx, success in enumerate(if_successes, start=1):
                rule = success.get('rule_demand', {})
                data = success.get('data_answer', {})
                success_text = (
                    f"{idx}. Question: {rule.get('question', 'N/A')}\n"
                    f"   Expected Answer: {rule.get('answer', 'N/A')}\n"
                    f"   Condition: {rule.get('condition', 'N/A')}\n"
                    f"   Actual Answer: {data.get('answers', 'N/A')}\n"
                    f"   Source: {rule.get('location', 'N/A')}\n"
                    f"   {'-' * 40}\n"
                )
                success_textbox.insert("end", success_text)

        # Confirmed THEN Rules
        then_successes = final_rule_dict.get("all_then_rules_confirmed", [])
        if then_successes:
            success_textbox.insert("end", "\nCONFIRMED THEN RULES:\n", "bold_green")
            success_textbox.insert("end", "===============\n", "bold_green")
            for idx, success in enumerate(then_successes, start=1):
                rule = success.get('rule_demand', {})
                data = success.get('data_answer', {})
                success_text = (
                    f"{idx}. Question: {rule.get('question', 'N/A')}\n"
                    f"   Expected: {rule.get('answer', 'N/A')}\n"
                    f"   Rule: {rule.get('condition', 'N/A')}\n"
                    f"   Actual Answer:: {data.get('answers', 'N/A')}\n"
                    f"   Source: {data.get('source', 'N/A')}\n"
                    f"   {'-' * 40}\n"
                )
                success_textbox.insert("end", success_text)

        success_textbox.configure(state="disabled")  # Make it read-only again

        # Update Failures Textbox
        failures_textbox.configure(state="normal")  # Enable editing
        failures_textbox.delete("1.0", "end")  # Clear existing content

        # Failed IF Rules (Displayed Before THEN Rules)
        if_failures = final_rule_dict.get("all_if_rules_failed", [])
        if if_failures:
            failures_textbox.insert("end", "FAILED IF RULE (won't bother checking other rules):\n", "bold_red")
            for idx, failure in enumerate(if_failures, start=1):
                rule = failure.get('rule_demand', {})
                data = failure.get('data_answer', {})
                failure_text = (
                    f"{idx}. Question: {rule.get('question', 'N/A')}\n"
                    f"   Expected Answer: {rule.get('answer', 'N/A')}\n"
                    f"   Condition Not Met: {rule.get('condition', 'N/A')}\n"
                    f"   Actual Answer: {data.get('answers', 'N/A')}\n"
                    f"   Source: {rule.get('location', 'N/A')}\n"
                    f"   {'-' * 40}\n"
                )
                failures_textbox.insert("end", failure_text)

        # Failed THEN Rules
        then_failures = final_rule_dict.get("all_then_rules_failed", [])
        if then_failures:
            failures_textbox.insert("end", "\nFAILED THEN RULES:\n", "bold_red")
            for idx, failure in enumerate(then_failures, start=1):
                rule = failure.get('rule_demand', {})
                data = failure.get('data_answer', {})
                failure_text = (
                    f"{idx}. Question: {rule.get('question', 'N/A')}\n"
                    f"   Expected: {rule.get('answer', 'N/A')}\n"
                    f"   Rule: {rule.get('condition', 'N/A')}\n"
                    f"   Actual Answer:: {data.get('answers', 'N/A')}\n"
                    f"   Source: {data.get('source', 'N/A')}\n"
                    f"   {'-' * 40}\n"
                )
                failures_textbox.insert("end", failure_text)

        failures_textbox.configure(state="disabled")  # Make it read-only again

    return update_validation_section
