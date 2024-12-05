import customtkinter as ctk
from tkinter import Scrollbar


def create_algemeen_tab(tab, algemeen_data):
    """
    Creates the Algemeen tab content with dynamic questions and answers.
    """
    if "data" in algemeen_data and isinstance(algemeen_data["data"], list):
        create_question_display(tab, algemeen_data["data"])
    else:
        label = ctk.CTkLabel(tab, text="No content available for Algemeen.")
        label.pack(pady=20)


def create_question_display(parent, questions_data):
    """
    Dynamically creates widgets to display questions and answers without scroll functionality.
    """
    # Create a frame to contain all question-answer pairs
    content_frame = ctk.CTkFrame(parent)
    content_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Create widgets for each question and answer
    for idx, question_data in enumerate(questions_data):
        question = question_data.get("question", "Unknown question")
        answers = question_data.get("answers", {})

        # Question Label
        question_frame = ctk.CTkFrame(content_frame)
        question_frame.pack(fill="x", pady=5, padx=10)

        question_label = ctk.CTkLabel(
            question_frame, text=question, anchor="w", wraplength=600, font=("Arial", 14)
        )
        question_label.pack(side="left", padx=10)

        question_button = ctk.CTkButton(
            question_frame,
            text="Print Question",
            command=lambda q=question: print_to_screen(f"Question: {q}"),
        )
        question_button.pack(side="right", padx=10)

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

            answer_button = ctk.CTkButton(
                answer_frame,
                text="Print Answer",
                command=lambda a=answer_text, v=answer_value: print_to_screen(
                    f"Answer: {a} -> {v}"
                ),
            )
            answer_button.pack(side="right", padx=10)



def print_to_screen(message):
    """
    Function to handle button clicks and print the message to the screen.
    """
    print(message)