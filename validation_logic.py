import re
import hyperSel
import hyperSel.colors_utilities
test_data = {
    "recording_tool": [
        {
            "data": [
                {
                    "question": "Welke situatie is van toepassing? De aanvrager is:",
                    "answers": {
                        "Particulier": True,
                        "Zakelijk": False,
                        "Gedeeltelijk particulier en gedeeltelijk zakelijk": False
                    }
                },
                {
                    "question": "Heeft de aanvrager voor zijn zakelijke prestaties recht op aftrek van de BTW?",
                    "answers": {
                        "Nee": True,
                        "Ja": False
                    }
                }
            ],
            "url": "https://productie.deatabix.nl/dossiers/9d78eecd-2f56-4ba3-a7b6-2482ed8ab37e/editors/deskundige/algemeen",
            "tab_type": "algemeen"
        },
        {
            "data": [
                {
                    "question": "Zijn met betrekking tot de ingevoerde schades één of meerdere kenmerken waargenomen waarbij mogelijk sprake is van ongelijke zetting?",
                    "answers": {
                        "Ja": True,
                        "Nee": True
                    }
                }
            ],
            "url": "https://productie.deatabix.nl/dossiers/9d78eecd-2f56-4ba3-a7b6-2482ed8ab37e/editors/deskundige/omgevingskenmerken",
            "tab_type": "omgevingskenmerken"
        },
        {
            "data": [
                {
                    "images": [
                        "https://deatabix-production-storage.s3.eu-central-1.amazonaws.com/media/9503e009-7714-4aa4-9475-95e88fc45d0c/img-logo.svg",
                        "https://www.gravatar.com/avatar/e1537c6a2f81cf9aac64d1362b2a93b3?d=identicon&s=128",
                        "https://deatabix-production-storage.s3.eu-central-1.amazonaws.com/media/f4361f34-153a-46d7-8e24-ffd450eb5f4b/conversions/image_picker_2461256f-thumbnail.jpg"
                    ],
                    "title": "G1.B1.R1. Overloop",
                    "questionaire_data": [
                        {
                            "question": "Wat is het oppervlakte (m2) van de vloer?",
                            "answers": "2.2"
                        },
                        {
                            "question": "Gebouw (verplicht)",
                            "answer": ""
                        },
                        {
                            "question": "Wil je een ruimte aan de binnenkant of buitenkant aanmaken?",
                            "answers": {
                                "Buitenkant gebouw": False,
                                "Binnenkant gebouw": True
                            }
                        },
                        {
                            "question": "Op welke bouwlaag bevind zich de ruimte?",
                            "answers": {
                                "Bouwlaag -1": False,
                                "Bouwlaag 0": False,
                                "Bouwlaag 0,5": False,
                                "Bouwlaag 1": True,
                                "Bouwlaag 2": False,
                                "Bouwlaag 3": False,
                                "Bouwlaag 4": False,
                                "Bouwlaag 5": False,
                                "Bouwlaag 6": False,
                                "Insteek": False
                            }
                        }
                    ]
                }
            ],
            "url": "https://productie.deatabix.nl/dossiers/9d78eecd-2f56-4ba3-a7b6-2482ed8ab37e/editors/deskundige/omgevingskenmerken",
            "tab_type": "omgevingskenmerken"
        }
    ],
    "control_tool": {
        "informatie": [
            {
                "question": "Algemene opmerking van de aanvrager",
                "answer": "-"
            },
            {
                "question": "Algemene opmerking van de deskundige",
                "answer": "Het gebouw betreft een appartement. Eventuele schade(s) aan de buitenmuren, het dak en/ of de fundering zijn niet meegenomen in de beoordeling van dit rapport, aangezien deze delen van het gebouw (totale complex) onder de verantwoordelijkheid van de Vereniging van Eigenaren vallen. In een aparte aanvraag kunnen deze schades (van het complex) worden aangevraagd."
            },
            {
                "question": "Welke situatie is van toepassing? De aanvrager is:",
                "answer": "Particulier"
            },
            {
                "question": "Heeft de aanvrager voor zijn zakelijke prestaties recht op aftrek van de BTW?",
                "answer": "Nee"
            },
            {
                "question": "Gebied",
                "answer": "Effectgebied"
            }
        ],
        "calculation": [
                {
                    "Naam": "Subtotaal G1.B1.R1. Overloop",
                    "Aantal": "",
                    "Stukprijs": "",
                    "Staffel": "",
                    "Ruimte": "",
                    "Gebouw": "€0,00",
                    "Totaal": "",
                    "BTW %": ""
                },
                {
                    "Naam": "Subtotaal G1.B1.R2. Berging",
                    "Aantal": "",
                    "Stukprijs": "",
                    "Staffel": "",
                    "Ruimte": "",
                    "Gebouw": "€0,00",
                    "Totaal": "",
                    "BTW %": ""
                },
                {
                    "Naam": "Subtotaal G1.B1.R3. Berging",
                    "Aantal": "",
                    "Stukprijs": "",
                    "Staffel": "",
                    "Ruimte": "",
                    "Gebouw": "€0,00",
                    "Totaal": "",
                    "BTW %": ""
                }
        ]
    }
}

example_validation_rule =     [
        {
            "type": "if",
            "question": "Heeft de aanvrager voor zijn zakelijke prestaties recht op aftrek van de BTW?",
            "answer": "Ja",
            "condition": False,
            "location": "algemeen"
        },
        {
            "type": "then",
            "question": "Welke situatie is van toepassing? De aanvrager is:",
            "answer": "Gedeeltelijk particulier en gedeeltelijk zakelijk",
            "condition": False,
            "location": "algemeen"
        }
    ]


def flatten_test_data_to_questions(data):
    flattened = []

    try:
        # Traverse recording_tool
        if "recording_tool" in data:
            for section in data["recording_tool"]:
                try:
                    source = section.get("tab_type", "unknown")
                    for entry in section.get("data", []):
                        try:
                            question = entry.get("question")
                            answers = entry.get("answers", {})
                            if question:
                                flattened.append({
                                    "question": question,
                                    "answers": answers,
                                    "source": source
                                })
                        except Exception as e:
                            hyperSel.colors_utilities.c_print(text=f"Error processing entry in 'data': {entry} - {e}", color="red")
                    for sub_entry in section.get("questionaire_data", []):
                        try:
                            question = sub_entry.get("question")
                            answers = sub_entry.get("answers", sub_entry.get("answer", {}))
                            if question:
                                flattened.append({
                                    "question": question,
                                    "answers": answers,
                                    "source": source
                                })
                        except Exception as e:
                            hyperSel.colors_utilities.c_print(text=f"Error processing sub_entry in 'questionaire_data': {sub_entry} - {e}", color="red")
                except Exception as e:
                    hyperSel.colors_utilities.c_print(text=f"Error processing section in 'recording_tool': {section} - {e}", color="red")

        # Traverse control_tool - informatie
        if "control_tool" in data and "informatie" in data["control_tool"]:
            for entry in data["control_tool"]["informatie"]:
                try:
                    question = entry.get("question")
                    answers = entry.get("answer", {})
                    if question:
                        flattened.append({
                            "question": question,
                            "answers": answers,
                            "source": "informatie"
                        })
                except Exception as e:
                    hyperSel.colors_utilities.c_print(text=f"Error processing entry in 'informatie': {entry} - {e}", color="red")

        # Traverse control_tool - calculation
        if "control_tool" in data and "calculation" in data["control_tool"]:
            for entry in data["control_tool"]["calculation"]:
                try:
                    question = entry.get("Naam")
                    answers = entry.get("Gebouw", "")
                    if question:
                        flattened.append({
                            "question": question,
                            "answers": answers,
                            "source": "calculation"
                        })
                except Exception as e:
                    hyperSel.colors_utilities.c_print(text=f"Error processing entry in 'calculation': {entry} - {e}", color="red")

    except Exception as e:
        hyperSel.colors_utilities.c_print(text=f"General error processing data: {data} - {e}", color="red")

    return flattened


def get_if_rules(selected_rule_set):
    if_rules = [rule for rule in selected_rule_set if rule.get("type") == "if"]
    return if_rules

def get_then_rules(selected_rule_set):
    then_rules = [rule for rule in selected_rule_set if rule.get("type") == "then"]
    return then_rules

def check_if_rule_in_data(rule, flattened_data):

    # Extract rule details
    rule_type = rule.get("type")
    rule_question = rule.get("question")
    rule_answer = rule.get("answer")
    rule_condition = rule.get("condition")
    rule_location = rule.get("location")

    #print("Rule Type:", rule_type)
    #print("Rule Question:", rule_question)
    #print("Rule Answer:", rule_answer)
    #print("Rule Condition:", rule_condition)
    #print("Rule Location:", rule_location)
    #print("==")

    rule_data_confirmed = []
    rule_data_failed = []
    rule_data_does_not_exist = []

    # Iterate through flattened data
    for data in flattened_data:
        question = data.get("question")
        answers = data.get("answers")
        source = data.get("source")

        # Attempt to convert answers to numbers if applicable
        if isinstance(answers, str):
            answers = convert_to_number(answers)
        elif isinstance(answers, dict):
            # Convert values in dict answers
            answers = {k: convert_to_number(v) for k, v in answers.items()}

        # Check if the question matches
        if question.lower() == rule_question.lower() and source == rule_location:
            #print("MATCH")
            #print("question:", question)
            #print("answers:", answers)
            #print("source:", source)

            # Check the type of `answers` and validate
            if isinstance(answers, dict):
                # If answers is a dictionary, check if the rule's answer exists and matches condition
                if rule_answer in answers and answers[rule_answer] == rule_condition:
                    # print("Rule confirmed!")
                    rule_data_confirmed.append(rule)
                else:
                    # print("Rule failed.")
                    rule_data_failed.append(rule)

            elif isinstance(answers, (list, str)):
                # Directly compare for lists or strings
                if answers == rule_answer:
                    #print("Rule confirmed!")
                    rule_data_confirmed.append(rule)
                else:
                    #print("Rule failed.")
                    rule_data_failed.append(rule)
            break
    else:
        # If no match is found in the data
        # print("Rule does not exist in the data.")
        rule_data_does_not_exist.append(rule)

    return {
        "confirmed": rule_data_confirmed,
        "failed": rule_data_failed,
        "not_found": rule_data_does_not_exist,
    }




def convert_to_number(value):
    """
    Attempts to convert a string value with potential currency symbols or formatting
    into a float. If conversion fails, returns the original value.
    """
    if isinstance(value, str):
        # Remove currency symbols and whitespace
        cleaned_value = re.sub(r'[^\d.,-]', '', value).strip()
        try:
            # Replace comma with dot for decimal handling (common in European formats)
            cleaned_value = cleaned_value.replace(',', '.') if ',' in cleaned_value and '.' not in cleaned_value else cleaned_value
            return float(cleaned_value)
        except ValueError:
            return value  # Return original value if conversion fails
    return value

def validation_rule_tool(current_data, selected_rule_set):
    flattened_data = flatten_test_data_to_questions(current_data)
    
    all_if_rules = get_if_rules(selected_rule_set)
    all_then_rules = get_then_rules(selected_rule_set)

    if len(all_then_rules) == 0:
        return []
    
    all_if_rules_confirmed = []
    all_if_rules_failed = []
    all_if_rules_not_found = []

    all_then_rules_confirmed = []
    all_then_rules_failed = []
    all_then_rules_not_found = []


    if len(all_if_rules) > 0:
        for if_rule in all_if_rules:

            rule_result_dict = check_if_rule_in_data(if_rule, flattened_data)
            rule_confirmed = rule_result_dict['confirmed']
            rule_failed = rule_result_dict['failed']
            rule_not_found = rule_result_dict['not_found']

            if rule_confirmed != []:
                all_if_rules_confirmed.append(rule_confirmed[0])

            if rule_failed != []:
                all_if_rules_failed.append(rule_failed[0])

            if rule_not_found != []:
                all_if_rules_not_found.append(rule_not_found[0])

        if len(all_if_rules_confirmed) != 0:
            for then_rule in all_then_rules:
                rule_result_dict = check_if_rule_in_data(then_rule, flattened_data)
                rule_confirmed = rule_result_dict['confirmed']
                rule_failed = rule_result_dict['failed']
                rule_not_found = rule_result_dict['not_found']

                if rule_confirmed != []:
                    all_then_rules_confirmed.append(rule_confirmed[0])

                if rule_failed != []:
                    all_then_rules_failed.append(rule_failed[0])

                if rule_not_found != []:
                    all_then_rules_not_found.append(rule_not_found[0])

    else:
        for then_rule in all_then_rules:
            rule_result_dict = check_if_rule_in_data(then_rule, flattened_data)
            rule_confirmed = rule_result_dict['confirmed']
            rule_failed = rule_result_dict['failed']
            rule_not_found = rule_result_dict['not_found']

            if rule_confirmed != []:
                all_then_rules_confirmed.append(rule_confirmed[0])

            if rule_failed != []:
                all_then_rules_failed.append(rule_failed[0])

            if rule_not_found != []:
                all_then_rules_not_found.append(rule_not_found[0])

    final_rule_dict = {
        "all_then_rules_confirmed":all_then_rules_confirmed,
        "all_then_rules_failed":all_then_rules_failed,
        "all_then_rules_not_found":all_then_rules_not_found,

        "all_if_rules_confirmed":all_if_rules_confirmed,
        "all_if_rules_failed":all_if_rules_failed,
        "all_if_rules_not_found":all_if_rules_not_found,

    }

    return final_rule_dict

if __name__ == '__main__':
    final_rule_dict = validation_rule_tool(current_data=test_data, selected_rule_set=example_validation_rule)
    for key, value in final_rule_dict.items():
        print(key)
        print(value)
        print("-")
