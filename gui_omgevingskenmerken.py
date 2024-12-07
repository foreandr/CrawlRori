import customtkinter as ctk
from tkinter import Toplevel
import validation_rules

def create_omgevingskenmerken_tab(tab, omgevingskenmerken_data):
    """
    Creates the Omgevingskenmerken tab content with dynamic questions and answers.
    """
    if "data" in omgevingskenmerken_data and isinstance(omgevingskenmerken_data["data"], list):
        create_question_display(tab, omgevingskenmerken_data["data"])
    else:
        label = ctk.CTkLabel(tab, text="No content available for Omgevingskenmerken.")
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
        answers = question_data.get("answers", {})

        # Question Section with Spacing
        question_label = ctk.CTkLabel(
            content_frame,
            text=question,
            anchor="w",
            wraplength=600,
            font=("Arial", 14, "bold"),  # Bold for clearer delineation
        )
        question_label.pack(fill="x", pady=(10, 5))  # Top padding for space between questions

        # Answer Section
        for answer_text, answer_value in answers.items():
            answer_frame = ctk.CTkFrame(content_frame)
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

def set_rule(rule_type, question, answer, value, rules):
    """
    Handles setting the "If" or "Then" rule with a boolean condition using a clickable dialog.
    """
    # Create a popup for boolean selection
    popup = Toplevel()
    popup.title(f"Set {rule_type.capitalize()} Rule")
    popup.geometry("300x150")
    popup.resizable(False, False)

    # Label
    label = ctk.CTkLabel(
        popup,
        text=f"Set condition for '{answer}' ({rule_type.upper()} Rule):",
        wraplength=280,
        anchor="center",
    )
    label.pack(pady=20)

    # Button for True
    true_button = ctk.CTkButton(
        popup,
        text="True",
        fg_color="green",
        command=lambda: finalize_rule(rule_type, question, answer, True, rules, popup),
    )
    true_button.pack(side="left", padx=20, pady=10)

    # Button for False
    false_button = ctk.CTkButton(
        popup,
        text="False",
        fg_color="red",
        command=lambda: finalize_rule(rule_type, question, answer, False, rules, popup),
    )
    false_button.pack(side="right", padx=20, pady=10)

def finalize_rule(rule_type, question, answer, condition, rules, popup):
    """
    Finalizes the rule, stores it, and closes the popup.
    """
    rule = {
        "type": rule_type,
        "question": question,
        "answer": answer,
        "condition": condition,
        "location": "omgevingskenmerken"
    }
    validation_rules.my_validation_rules.append(rule)

    rules.append(rule)  # Store the rule
    print(f"Rule set: {rule}")
    popup.destroy()  # Close the popup
