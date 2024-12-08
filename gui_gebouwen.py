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
            

def set_rule(rule_type, question, target, rules, value=None):
    """
    Handles setting the "If" or "Then" rule with specific logic for strings and numbers.
    """
    # Create a popup for rule selection
    popup = Toplevel()
    popup.title(f"Set {rule_type.capitalize()} Rule")
    popup.geometry("350x350")
    popup.resizable(False, False)

    # Label for the popup
    label = ctk.CTkLabel(
        popup,
        text=f"Set condition for '{target}' ({rule_type.upper()} Rule):",
        wraplength=280,
        anchor="center",
        text_color="black"  # Set the text color to black
    )
    label.pack(pady=10)

    detected_type = detect_data_type(rule_type, question, target, value, rules)
    print("detected_type:", detected_type)

    if detected_type == "number":
        # Input for numeric comparison
        input_entry = ctk.CTkEntry(popup, placeholder_text="Enter a numeric value")
        input_entry.pack(pady=10)

        greater_button = ctk.CTkButton(
            popup,
            text="Greater Than",
            command=lambda: finalize_rule(
                rule_type, question, target, {">": input_entry.get()}, rules, popup
            ),
        )
        greater_button.pack(pady=5)

        less_button = ctk.CTkButton(
            popup,
            text="Less Than",
            command=lambda: finalize_rule(
                rule_type, question, target, {"<": input_entry.get()}, rules, popup
            ),
        )
        less_button.pack(pady=5)

        equal_button = ctk.CTkButton(
            popup,
            text="Equal To",
            command=lambda: finalize_rule(
                rule_type, question, target, {"=": input_entry.get()}, rules, popup
            ),
        )
        equal_button.pack(pady=5)

    elif detected_type == "boolean":
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

    else:  # Detected type is string
        input_entry = ctk.CTkEntry(popup, placeholder_text="Enter substring")
        input_entry.pack(pady=10)

        contains_button = ctk.CTkButton(
            popup,
            text="Contains",
            command=lambda: finalize_rule(
                rule_type, question, target, {"contains": input_entry.get()}, rules, popup
            ),
        )
        contains_button.pack(pady=10)



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
    # Ensure numeric input is valid
    if isinstance(condition, dict) and list(condition.keys())[0] in [">", "<", "="]:
        try:
            operator = list(condition.keys())[0]
            value = float(condition[operator])  # Convert to float
            condition = {operator: value}  # Store as numeric
        except ValueError:
            print("Invalid numeric input")
            popup.destroy()
            return

    # Create the rule
    rule = {
        "type": rule_type,
        "question": question,
        "answer": answer,
        "condition": condition,
        "location": "gebouwen",
    }
    validation_rules.my_validation_rules.append(rule)

    # rules.append(rule)  # Store the rule locally
    print(f"Rule set: {rule}")
    popup.destroy()  # Close the popup


def detect_data_type(rule_type, question, target, value, rules):
    '''
    print("=====")
    print("rule_type:", rule_type)
    print("question :", question)
    print("target   :", target)
    print("rules    :", rules)
    print("value    :", value)
    '''

    item_to_check = None
    if rules == None:
        item_to_check = target
    else:
        item_to_check = rules
        
    # Check for boolean
    if isinstance(item_to_check, bool):
        return "boolean"

    # Check if it's numeric (can be cast to float)
    if is_numeric(item_to_check):
        return "number"

    # Default to string
    return "string"