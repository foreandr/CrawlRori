import customtkinter as ctk
from tkinter import Toplevel
import validation_rules


def create_ruimtes_tab(tab, ruimtes_data):
    """
    Creates the Ruimtes tab content with dynamic tabs for each ruimte.
    """
    if "data" in ruimtes_data and isinstance(ruimtes_data["data"], list):
        # Create a TabView inside the main tab
        main_tabview = ctk.CTkTabview(tab)
        main_tabview.pack(fill="both", expand=True, padx=10, pady=10)

        # Loop through each ruimte in the data
        for ruimte_data in ruimtes_data["data"]:
            ruimte_title = ruimte_data.get("title", "Unknown Ruimte")
            ruimte_tab = main_tabview.add(ruimte_title)

            # Populate each tab with ruimte-specific content
            create_ruimte_display(ruimte_tab, ruimte_data)
    else:
        label = ctk.CTkLabel(tab, text="No content available for Ruimtes.")
        label.pack(pady=20)


def create_ruimte_display(parent, ruimte_data):
    """
    Creates the UI for an individual ruimte.
    """
    # Scrollable frame to display ruimte details
    scrollable_frame = ctk.CTkScrollableFrame(parent, width=900, height=600, corner_radius=10)
    scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Display ruimte title
    ruimte_title = ruimte_data.get("title", "Unknown Ruimte")
    ctk.CTkLabel(scrollable_frame, text=f"Ruimte: {ruimte_title}", font=("Arial", 16, "bold")).pack(pady=(10, 5))

    # Display images
    #images = ruimte_data.get("images", [])
    #if images:
    #    create_image_display(scrollable_frame, images)

    # Display questionnaire data
    questionnaire_data = ruimte_data.get("questionaire_data", [])
    if questionnaire_data:
        create_questionnaire_display(scrollable_frame, questionnaire_data)
    else:
        ctk.CTkLabel(scrollable_frame, text="No questionnaire data available.").pack(pady=20)


def create_image_display(parent, images):
    """
    Displays a list of images with clickable links.
    """
    ctk.CTkLabel(parent, text="Images:", font=("Arial", 14, "bold")).pack(pady=(10, 5))
    for image_url in images:
        image_label = ctk.CTkLabel(parent, text=image_url, fg_color="transparent", text_color="blue", cursor="hand2")
        image_label.pack(anchor="w", padx=10)
        image_label.bind("<Button-1>", lambda e, url=image_url: open_image(url))


def open_image(image_url):
    """
    Opens the image URL in the default web browser.
    """
    import webbrowser
    webbrowser.open(image_url)


def create_questionnaire_display(parent, questions_data):
    """
    Dynamically creates widgets to display questionnaire data with "If Rule" and "Then Rule" buttons.
    """
    rules = []

    for idx, question_data in enumerate(questions_data):
        question = question_data.get("question", "Unknown question")
        answers = question_data.get("answers", {})

        # Question Section
        question_label = ctk.CTkLabel(parent, text=question, anchor="w", wraplength=800, font=("Arial", 14, "bold"))
        question_label.pack(fill="x", pady=(10, 5))

        if isinstance(answers, dict):
            for answer_text, answer_value in answers.items():
                answer_frame = ctk.CTkFrame(parent)
                answer_frame.pack(fill="x", padx=20, pady=2)

                answer_label = ctk.CTkLabel(answer_frame, text=f"{answer_text}: {'✔️' if answer_value else '❌'}", anchor="w")
                answer_label.pack(side="left", padx=10)

                # Add "Then Rule" Button
                ctk.CTkButton(
                    answer_frame,
                    text="Then Rule",
                    command=lambda q=question, a=answer_text, v=answer_value: set_rule("then", q, a, v, rules),
                ).pack(side="right", padx=10)

                # Add "If Rule" Button
                ctk.CTkButton(
                    answer_frame,
                    text="If Rule",
                    command=lambda q=question, a=answer_text, v=answer_value: set_rule("if", q, a, v, rules),
                ).pack(side="right", padx=10)

        else:
            answer_frame = ctk.CTkFrame(parent)
            answer_frame.pack(fill="x", padx=20, pady=2)

            answer_label = ctk.CTkLabel(answer_frame, text=f"Answer: {answers}", anchor="w")
            answer_label.pack(side="left", padx=10)

            # Add "Then Rule" Button
            ctk.CTkButton(
                answer_frame,
                text="Then Rule",
                command=lambda q=question, a=answers: set_rule("then", q, a, None, rules),
            ).pack(side="right", padx=10)

            # Add "If Rule" Button
            ctk.CTkButton(
                answer_frame,
                text="If Rule",
                command=lambda q=question, a=answers: set_rule("if", q, a, None, rules),
            ).pack(side="right", padx=10)


def set_rule(rule_type, question, target, value, rules):
    """
    Handles setting the "If" or "Then" rule with specific logic.
    """
    popup = Toplevel()
    popup.title(f"Set {rule_type.capitalize()} Rule")
    popup.geometry("350x350")
    popup.resizable(False, False)

    label = ctk.CTkLabel(popup, text=f"Set condition for '{target}' ({rule_type.upper()} Rule):", wraplength=280)
    label.pack(pady=10)

    detected_type = detect_data_type(target)
    if detected_type == "number":
        input_entry = ctk.CTkEntry(popup, placeholder_text="Enter a numeric value")
        input_entry.pack(pady=10)
        ctk.CTkButton(popup, text="Greater Than", command=lambda: finalize_rule(rule_type, question, target, {">": input_entry.get()}, rules, popup)).pack(pady=5)
        ctk.CTkButton(popup, text="Less Than", command=lambda: finalize_rule(rule_type, question, target, {"<": input_entry.get()}, rules, popup)).pack(pady=5)
        ctk.CTkButton(popup, text="Equal To", command=lambda: finalize_rule(rule_type, question, target, {"=": input_entry.get()}, rules, popup)).pack(pady=5)

    elif detected_type == "boolean":
        ctk.CTkButton(popup, text="True", fg_color="green", command=lambda: finalize_rule(rule_type, question, target, True, rules, popup)).pack(side="left", padx=20, pady=10)
        ctk.CTkButton(popup, text="False", fg_color="red", command=lambda: finalize_rule(rule_type, question, target, False, rules, popup)).pack(side="right", padx=20, pady=10)

    else:
        input_entry = ctk.CTkEntry(popup, placeholder_text="Enter substring")
        input_entry.pack(pady=10)
        ctk.CTkButton(popup, text="Contains", command=lambda: finalize_rule(rule_type, question, target, {"contains": input_entry.get()}, rules, popup)).pack(pady=10)


def finalize_rule(rule_type, question, target, condition, rules, popup):
    """
    Finalizes the rule and closes the popup.
    """
    rule = {
        "type": rule_type,
        "question": question,
        "answer": target,
        "condition": condition,
        "location": "ruimtes"
    }
    validation_rules.my_validation_rules.append(rule)
    print(f"Rule set: {rule}")
    popup.destroy()


def detect_data_type(value):
    """
    Detects the data type of the value.
    """
    if isinstance(value, bool):
        return "boolean"
    try:
        float(value)
        return "number"
    except (ValueError, TypeError):
        return "string"
