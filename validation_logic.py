import re

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
            ]
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

    # Traverse recording_tool
    if "recording_tool" in data:
        for section in data["recording_tool"]:
            source = section.get("tab_type", "unknown")
            for entry in section.get("data", []):
                question = entry.get("question")
                answers = entry.get("answers", {})
                if question:
                    flattened.append({
                        "question": question,
                        "answers": answers,
                        "source": source
                    })
            for sub_entry in section.get("questionaire_data", []):
                question = sub_entry.get("question")
                answers = sub_entry.get("answers", sub_entry.get("answer", {}))
                if question:
                    flattened.append({
                        "question": question,
                        "answers": answers,
                        "source": source
                    })

    # Traverse control_tool - informatie
    if "control_tool" in data and "informatie" in data["control_tool"]:
        for entry in data["control_tool"]["informatie"]:
            question = entry.get("question")
            answers = entry.get("answer", {})
            if question:
                flattened.append({
                    "question": question,
                    "answers": answers,
                    "source": "informatie"
                })

    # Traverse control_tool - calculation
    if "control_tool" in data and "calculation" in data["control_tool"]:
        for entry in data["control_tool"]["calculation"]:
            question = entry.get("Naam")
            answers = entry.get("Gebouw", "")
            if question:
                flattened.append({
                    "question": question,
                    "answers": answers,
                    "source": "calculation"
                })

    return flattened

def get_if_rules(selected_rule_set):
    if_rules = [rule for rule in selected_rule_set if rule.get("type") == "if"]
    return if_rules

def get_then_rules(selected_rule_set):
    then_rules = [rule for rule in selected_rule_set if rule.get("type") == "then"]
    return then_rules

def check_if_rule_in_data(rule, flattened_data):

    rule_type = rule.get("type")
    rule_question = rule.get("question")
    rule_answer = rule.get("answer")
    rule_condition = rule.get("condition")
    rule_location = rule.get("location")

    for data in flattened_data:
        question = data.get('question')
        answers = data.get('answers')
        source = data.get('source')

        # Attempt to convert answers to numbers if possible
        if isinstance(answers, str):
            answers = convert_to_number(answers)
        elif isinstance(answers, dict):
            # Convert values in dict answers
            answers = {k: convert_to_number(v) for k, v in answers.items()}

        print("question:", question)
        print("answers:", answers)
        print("source:", source)
        print("--")
    pass
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

def clean_data_from_each_section(current_data, selected_rule_set):
    flattened_data = flatten_test_data_to_questions(current_data)
    
    all_if_rules = get_if_rules(selected_rule_set)
    all_then_rules = get_then_rules(selected_rule_set)

    if len(all_then_rules) == 0:
        print("NO RULES, RETURN NOTHING")
        return []
    

    if len(all_if_rules) > 0:
        print("WE HAVE IF RULES")
        if_rule_in_data = None
        for if_rule in all_if_rules:
            if_rule_exists_in_data = check_if_rule_in_data(if_rule, flattened_data)
            print("if_rule:", if_rule)
        exit()


    else:
        print("JUST CHECK THE THEN RULES")

    exit()
    for i in flattened_data:
        print(i)

if __name__ == '__main__':
    res = clean_data_from_each_section(current_data=test_data, selected_rule_set=example_validation_rule)
