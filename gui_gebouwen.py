import customtkinter as ctk
from tkinter import Toplevel
import validation_rules


def create_gebouwen_tab(tab, gebouwen_data):
    """
    Creates the Gebouwen tab content with dynamic tabs for each building.
    """
    if "data" in gebouwen_data and isinstance(gebouwen_data["data"], list):
        # Create a TabView inside the main tab
        main_tabview = ctk.CTkTabview(tab)  # Corrected capitalization
        main_tabview.pack(fill="both", expand=True, padx=10, pady=10)

        # Loop through each building in the data
        for building_data in gebouwen_data["data"]:
            building_title = building_data.get("building_title", "Unknown Building")
            building_tab = main_tabview.add(building_title)

            # Populate each tab with building-specific content
            create_building_display(building_tab, building_data)
    else:
        label = ctk.CTkLabel(tab, text="No content available for Gebouwen.")
        label.pack(pady=20)


def create_building_display(parent, building_data):
    """
    Creates the UI for an individual building.
    """
    # Display building details in a scrollable frame
    scrollable_frame = ctk.CTkScrollableFrame(parent, width=900, height=600, corner_radius=10)
    scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Display building title
    building_title = building_data.get("building_title", "Unknown Building")
    ctk.CTkLabel(scrollable_frame, text=f"Building: {building_title}", font=("Arial", 16, "bold")).pack(pady=(10, 5))

    questions_data = building_data.get("questions_data", [])
    if questions_data:
        create_question_display(scrollable_frame, questions_data)
    else:
        ctk.CTkLabel(scrollable_frame, text="No questions available.").pack(pady=20)


def create_question_display(parent, questions_data):
    """
    Dynamically creates widgets to display questions and answers with "If Rule" and "Then Rule" buttons.
    """
    # Data structure to store rules
    rules = []

    # Create widgets for each question and answer
    for idx, question_data in enumerate(questions_data):
        question = question_data.get("question", "Unknown question")
        answers = question_data.get("answers", {})

        # Question Section
        question_label = ctk.CTkLabel(
            parent,
            text=question,
            anchor="w",
            wraplength=800,
            font=("Arial", 14, "bold"),
        )
        question_label.pack(fill="x", pady=(10, 5))

        if isinstance(answers, dict):
            for answer_text, answer_value in answers.items():
                answer_frame = ctk.CTkFrame(parent)
                answer_frame.pack(fill="x", padx=20, pady=2)

                answer_label = ctk.CTkLabel(
                    answer_frame,
                    text=f"{answer_text}: {'✔️' if answer_value else '❌'}",
                    anchor="w",
                )
                answer_label.pack(side="left", padx=10)

                # Add "Then Rule" Button
                then_rule_button = ctk.CTkButton(
                    answer_frame,
                    text="Then Rule",
                    command=lambda q=question, a=answer_text, v=answer_value: set_rule("then", q, a, v, rules),
                )
                then_rule_button.pack(side="right", padx=10)

                # Add "If Rule" Button
                if_rule_button = ctk.CTkButton(
                    answer_frame,
                    text="If Rule",
                    command=lambda q=question, a=answer_text, v=answer_value: set_rule("if", q, a, v, rules),
                )
                if_rule_button.pack(side="right", padx=10)


        else:
            # Handle non-dict answers (e.g., strings or numbers)
            answer_frame = ctk.CTkFrame(parent)
            answer_frame.pack(fill="x", padx=20, pady=2)

            answer_label = ctk.CTkLabel(
                answer_frame,
                text=f"Answer: {answers}",
                anchor="w",
            )
            answer_label.pack(side="left", padx=10)

            # Add "Then Rule" Button
            then_rule_button = ctk.CTkButton(
                answer_frame,
                text="Then Rule",
                command=lambda q=question, a=answers: set_rule("then", q, a, None, rules),
            )
            then_rule_button.pack(side="right", padx=10)

            # Add "If Rule" Button
            if_rule_button = ctk.CTkButton(
                answer_frame,
                text="If Rule",
                command=lambda q=question, a=answers: set_rule("if", q, a, None, rules),
            )
            if_rule_button.pack(side="right", padx=10)
            

def set_rule(rule_type, question, answer, value, rules):
    """
    Handles setting the "If" or "Then" rule with specific logic for strings, numbers, and booleans.
    """
    # Fallback logic: Check value, then fallback to answer if value is None
    target = value if value is not None else answer

    # Determine the type of the target
    if target is None or target == "":
        value_type = "none"
    elif isinstance(target, bool):
        value_type = "boolean"
    elif isinstance(target, (int, float)) and not isinstance(target, bool):
        value_type = "number"
    elif isinstance(target, str):
        try:
            # Check if the string can be converted to a number
            float(target)
            value_type = "number"
        except ValueError:
            value_type = "string"
    else:
        value_type = "unknown"

    # Debug print to show the type
    print(f"DEBUG: Answer = {answer}, Value = {value}, Target = {target}, Detected Type = {value_type}")

    # Create the popup for rule selection
    popup = Toplevel()
    popup.title(f"Set {rule_type.capitalize()} Rule")
    popup.geometry("300x200")
    popup.resizable(False, False)

    label = ctk.CTkLabel(
        popup,
        text=f"Set condition for '{target}' ({rule_type.upper()} Rule):",
        wraplength=280,
        anchor="center",
    )
    label.pack(pady=20)

    # Handle logic based on type
    if value_type == "number":
        # Provide numeric comparison options
        greater_button = ctk.CTkButton(
            popup,
            text="Greater Than",
            command=lambda: finalize_rule(rule_type, question, target, ">", rules, popup),
        )
        greater_button.pack(side="top", pady=5)

        less_button = ctk.CTkButton(
            popup,
            text="Less Than",
            command=lambda: finalize_rule(rule_type, question, target, "<", rules, popup),
        )
        less_button.pack(side="top", pady=5)

        equal_button = ctk.CTkButton(
            popup,
            text="Equal To",
            command=lambda: finalize_rule(rule_type, question, target, "=", rules, popup),
        )
        equal_button.pack(side="top", pady=5)

    elif value_type == "string":
        # Provide "contains" logic for strings
        contains_label = ctk.CTkLabel(
            popup,
            text="Enter a value to check if the string contains:",
        )
        contains_label.pack(pady=10)

        input_entry = ctk.CTkEntry(popup, placeholder_text="Enter substring")
        input_entry.pack(pady=10)

        confirm_button = ctk.CTkButton(
            popup,
            text="Confirm",
            command=lambda: finalize_rule(
                rule_type,
                question,
                target,
                {"operator": "contains", "value": input_entry.get()},
                rules,
                popup,
            ),
        )
        confirm_button.pack(pady=10)

    elif value_type == "boolean":
        # Provide True/False options for booleans
        true_button = ctk.CTkButton(
            popup,
            text="True",
            fg_color="green",
            command=lambda: finalize_rule(rule_type, question, target, True, rules, popup),
        )
        true_button.pack(side="left", padx=20, pady=10)

        false_button = ctk.CTkButton(
            popup,
            text="False",
            fg_color="red",
            command=lambda: finalize_rule(rule_type, question, target, False, rules, popup),
        )
        false_button.pack(side="right", padx=20, pady=10)

    else:
        # If the type is unknown, show an error message
        error_label = ctk.CTkLabel(
            popup,
            text="Unsupported or unknown type.",
        )
        error_label.pack(pady=20)

        close_button = ctk.CTkButton(
            popup,
            text="Close",
            command=popup.destroy,
        )
        close_button.pack(pady=10)


def is_numeric(value):
    """
    Determines if the provided value can be cast to a number (int or float).
    """
    try:
        float(value)  # Attempt to cast to a float
        return True
    except (ValueError, TypeError):
        return False

def finalize_rule(rule_type, question, answer, condition, rules, popup):
    """
    Finalizes the rule, stores it in the rules list, and closes the popup.
    """
    rule = {
        "type": rule_type,
        "question": question,
        "answer": answer,
        "condition": condition,
        "location": "gebouwen",  # Example of additional context
    }
    # Add the rule to your validation rules
    validation_rules.my_validation_rules.append(rule)
    rules.append(rule)  # Store the rule locally for reference
    print(f"Rule set: {rule}")
    popup.destroy()  # Close the popup