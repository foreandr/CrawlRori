import customtkinter as ctk
from tkinter import Toplevel
import validation_rules

def create_samenvatting_tab(tab, samenvatting_data):
    """
    Creates the Samenvatting tab content with dynamic questions and answers.
    """
    if "data" in samenvatting_data and isinstance(samenvatting_data["data"], list):
        create_question_display(tab, samenvatting_data["data"])
    else:
        label = ctk.CTkLabel(tab, text="No content available for Samenvatting.")
        label.pack(pady=20)

def create_question_display(parent, questions_data):
    """
    Dynamically creates widgets to display questions and answers with "If Rule" and "Then Rule" buttons.
    """
    # Create a frame to contain all question-answer pairs
    content_frame = ctk.CTkFrame(parent)
    content_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Data structure to store rules
    rules = []

    # Create widgets for each question and answer
    for idx, question_data in enumerate(questions_data):
        question = question_data.get("question", "Unknown question")
        answer = question_data.get("answer", "No answer provided")

        # Question Section with Spacing
        question_label = ctk.CTkLabel(
            content_frame,
            text=question,
            anchor="w",
            wraplength=600,
            font=("Arial", 14, "bold"),
        )
        question_label.pack(fill="x", pady=(10, 5))

        # Answer Section
        answer_frame = ctk.CTkFrame(content_frame)
        answer_frame.pack(fill="x", padx=20, pady=5)

        answer_label = ctk.CTkLabel(
            answer_frame,
            text=f"Answer: {answer}",
            anchor="w",
        )
        answer_label.pack(side="left", padx=10)

        # Add "Then Rule" Button
        then_rule_button = ctk.CTkButton(
            answer_frame,
            text="Then Rule",
            command=lambda q=question, a=answer: set_rule("then", q, a, rules),
        )
        then_rule_button.pack(side="right", padx=10)

        # Add "If Rule" Button
        if_rule_button = ctk.CTkButton(
            answer_frame,
            text="If Rule",
            command=lambda q=question, a=answer: set_rule("if", q, a, rules),
        )
        if_rule_button.pack(side="right", padx=10)

def set_rule(rule_type, question, target, rules):
    """
    Handles setting the "If" or "Then" rule with appropriate options based on data type.
    """
    popup = Toplevel()
    popup.title(f"Set {rule_type.capitalize()} Rule")
    popup.geometry("350x350")
    popup.resizable(False, False)

    label = ctk.CTkLabel(
        popup,
        text=f"Set condition for '{target}' ({rule_type.upper()} Rule):",
        wraplength=280,
        anchor="center",
    )
    label.pack(pady=10)

    detected_type = detect_data_type(target)
    print("Detected type:", detected_type)

    if detected_type == "number":
        input_entry = ctk.CTkEntry(popup, placeholder_text="Enter a numeric value")
        input_entry.pack(pady=10)
        ctk.CTkButton(
            popup,
            text="Greater Than",
            command=lambda: finalize_rule(rule_type, question, target, {">": input_entry.get()}, rules, popup),
        ).pack(pady=5)
        ctk.CTkButton(
            popup,
            text="Less Than",
            command=lambda: finalize_rule(rule_type, question, target, {"<": input_entry.get()}, rules, popup),
        ).pack(pady=5)
        ctk.CTkButton(
            popup,
            text="Equal To",
            command=lambda: finalize_rule(rule_type, question, target, {"=": input_entry.get()}, rules, popup),
        ).pack(pady=5)

    elif detected_type == "boolean":
        ctk.CTkButton(
            popup,
            text="True",
            fg_color="green",
            command=lambda: finalize_rule(rule_type, question, target, True, rules, popup),
        ).pack(side="left", padx=20, pady=10)
        ctk.CTkButton(
            popup,
            text="False",
            fg_color="red",
            command=lambda: finalize_rule(rule_type, question, target, False, rules, popup),
        ).pack(side="right", padx=20, pady=10)

    else:
        input_entry = ctk.CTkEntry(popup, placeholder_text="Enter substring")
        input_entry.pack(pady=10)
        ctk.CTkButton(
            popup,
            text="Contains",
            command=lambda: finalize_rule(rule_type, question, target, {"contains": input_entry.get()}, rules, popup),
        ).pack(pady=10)

def finalize_rule(rule_type, question, target, condition, rules, popup):
    """
    Finalizes the rule, stores it, and closes the popup.
    """
    rule = {
        "type": rule_type,
        "question": question,
        "answer": target,
        "condition": condition,
        "location": "samenvatting"
    }
    validation_rules.my_validation_rules.append(rule)

    rules.append(rule)
    print(f"Rule set: {rule}")
    popup.destroy()

def is_numeric(value):
    """
    Determines if the provided value can be cast to a number (int or float).
    """
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False

def detect_data_type(target):
    """
    Detects the data type of the target.
    """
    if isinstance(target, bool):
        return "boolean"
    if is_numeric(target):
        return "number"
    return "string"
