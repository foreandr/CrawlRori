import hyperSel
import hyperSel.log_utilities
import custom_log

data = custom_log.read_from_file("./logs/crawl_data.json")
#print(data)
item = data[0]
print(item.keys())
print("=================")
# print(item)

def extract_question_answer_pairs(data):
    question_answer_pairs = []

    def traverse(obj):
        # Check if the object is a dictionary
        if isinstance(obj, dict):
            # Check if it has "question" and "answers" keys
            if "question" in obj and "answers" in obj:
                # Validate that "answers" is a dictionary
                if isinstance(obj["answers"], dict):
                    question_answer_pairs.append({
                        "question": obj["question"],
                        "answers": obj["answers"]
                    })
            else:
                # Recursively traverse nested dictionaries
                for key, value in obj.items():
                    traverse(value)
        # Check if the object is a list
        elif isinstance(obj, list):
            # Recursively traverse each item in the list
            for item in obj:
                traverse(item)

    # Start traversing from the root data
    traverse(data)
    return question_answer_pairs

list_of_questions = extract_question_answer_pairs(item)

for i, data in enumerate(list_of_questions):
    print(i, data)