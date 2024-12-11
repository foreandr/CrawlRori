import customtkinter as ctk
from tkinter import Toplevel
import validation_rules


def create_schades_tab(tab, schades_data):
    """
    Creates the Schades tab content with dynamic tabs for each schade, adding pagination to limit the number of visible tabs.
    """
    if "data" in schades_data and isinstance(schades_data["data"], list):
        # Pagination variables
        items_per_page = 5  # Number of tabs to display per page
        total_items = len(schades_data["data"])
        total_pages = (total_items + items_per_page - 1) // items_per_page  # Ceiling division
        current_page = [0]  # Use a mutable object to allow updates in nested functions

        # Track tabs manually
        tabs_list = []

        # Create a frame for the pagination controls
        pagination_frame = ctk.CTkFrame(tab)
        pagination_frame.pack(fill="x", padx=10, pady=5)

        # Create the main TabView for Schades
        main_tabview = ctk.CTkTabview(tab)
        main_tabview.pack(fill="both", expand=True, padx=10, pady=10)

        # Debug: Ensure we are working with the correct main_tabview
        #print("main_tabview initialized.")

        def load_page(page):
            """
            Load a specific page of tabs, updating the displayed tabs and pagination controls.
            """
            nonlocal current_page, tabs_list
            current_page[0] = page

            # Print the page being loaded
            #print(f"Loading page {page + 1} with tabs from index {page * items_per_page} to {min((page + 1) * items_per_page, total_items)}")

            # Clear existing tabs
            for tab_name in tabs_list:
                main_tabview.delete(tab_name)
            tabs_list = []  # Reset the tabs list

            # Determine the range of items to display
            start_idx = page * items_per_page
            end_idx = min(start_idx + items_per_page, total_items)

            for i in range(start_idx, end_idx):
                schade_data = schades_data["data"][i]
                schade_title = schade_data.get("title", f"Schade {i + 1}")
                tabs_list.append(schade_title)  # Track the tab name
                main_tabview.add(schade_title)

            update_pagination_controls()

        def on_tab_change():
            """
            Function to handle tab change.
            Called whenever a new tab is clicked.
            """
            selected_tab = main_tabview.get()  # Get the currently selected tab
            #print(f"Tab clicked: {selected_tab}")  # Debug print to confirm the new tab
            lazy_load_tab_content()  # Load content dynamically for the selected tab

        def lazy_load_tab_content():
            """
            Lazy-load content for the currently selected tab.
            """
            selected_tab = main_tabview.get()  # Get currently selected tab
            if selected_tab not in tabs_list:
                return  # Skip if the tab isn't in the tracked list

            # Print the tab being loaded
            #print(f"Loading data for tab: {selected_tab}")

            # Find the corresponding schade data by title
            for schade_data in schades_data["data"]:
                if schade_data.get("title", "Unknown Schade") == selected_tab:
                    schade_tab = main_tabview.tab(selected_tab)
                    create_schade_display(schade_tab, schade_data)
                    break

        def update_pagination_controls():
            """
            Update the pagination buttons based on the current page.
            """
            for widget in pagination_frame.winfo_children():
                widget.destroy()

            # Add "Previous" button
            if current_page[0] > 0:
                ctk.CTkButton(
                    pagination_frame,
                    text="Previous",
                    command=lambda: load_page(current_page[0] - 1),
                ).pack(side="left", padx=5)

            # Add "Next" button
            if current_page[0] < total_pages - 1:
                ctk.CTkButton(
                    pagination_frame,
                    text="Next",
                    command=lambda: load_page(current_page[0] + 1),
                ).pack(side="right", padx=5)

            # Add page info
            ctk.CTkLabel(
                pagination_frame,
                text=f"Page {current_page[0] + 1} of {total_pages}",
                anchor="center",
            ).pack(side="left", expand=True)

        def monitor_tab_selection():
            """
            Continuously monitor the selected tab and call `on_tab_change` if it changes.
            """
            previous_tab = [None]  # Mutable to track the last selected tab

            def check_tab():
                current_tab = main_tabview.get()
                if current_tab != previous_tab[0]:  # Tab has changed
                    previous_tab[0] = current_tab
                    on_tab_change()  # Trigger the tab change handler
                main_tabview.after(100, check_tab)  # Check again after 100ms

            check_tab()  # Start monitoring

        # Load the first page
        load_page(0)

        # Start monitoring for tab selection changes
        monitor_tab_selection()

    else:
        label = ctk.CTkLabel(tab, text="No content available for Schades.")
        label.pack(pady=20)


def create_schade_display(parent, schade_data):
    """
    Creates the UI for an individual schade.
    """
    # Print the schade being displayed
    schade_title = schade_data.get("title", "Unknown Schade")
    print(f"Creating display for: {schade_title}")

    # Scrollable frame to display schade details
    scrollable_frame = ctk.CTkScrollableFrame(parent, width=900, height=600, corner_radius=10)
    scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Display schade title
    ctk.CTkLabel(scrollable_frame, text=f"Schade: {schade_title}", font=("Arial", 16, "bold")).pack(pady=(10, 5))

    # Display questionnaire data
    questionaire_data = schade_data.get("questionaire_data", [])
    if questionaire_data:
        create_questionnaire_display(scrollable_frame, questionaire_data)
    else:
        ctk.CTkLabel(scrollable_frame, text="No questionnaire data available.").pack(pady=20)


def create_questionnaire_display(parent, questions_data):
    """
    Dynamically creates widgets to display questionnaire data with "If Rule" and "Then Rule" buttons.
    """
    rules = []

    for idx, question_data in enumerate(questions_data):
        question = question_data.get("question", "Unknown question")
        answers = question_data.get("answers", {})

        # print(f"Displaying question: {question}")

        # Question Section
        question_label = ctk.CTkLabel(parent, text=question, anchor="w", wraplength=800, font=("Arial", 14, "bold"))
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

def finalize_rule(rule_type, question, target, condition, rules, popup):
    """
    Finalizes the rule and closes the popup.
    """
    rule = {
        "type": rule_type,
        "question": question,
        "answer": target,
        "condition": condition,
        "location": "schades",
    }
    validation_rules.my_validation_rules.append(rule)
    print(f"Rule set: {rule}")
    popup.destroy()


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
    if rules == None or rules == []:
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


def is_numeric(value):
    """
    Determines if the provided value can be cast to a number (int or float).
    """
    try:
        float(value)  # Attempt to cast to a float
        return True
    except (ValueError, TypeError):
        return False
