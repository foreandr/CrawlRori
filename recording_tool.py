import hyperSel
import hyperSel.selenium_utilities
import hyperSel.log_utilities
import hyperSel.colors_utilities
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import custom_log

def recording_tool_crawl(driver, url):
    print("DOING RECORDING TOOL")
    hyperSel.selenium_utilities.go_to_site(driver, url)
    tab_data = single_dossier_iteration(driver)
    return tab_data
    
def single_dossier_iteration(driver):
    # print("single_dossier_iteration")
    dossier_xpath = '''/html/body/div/div[1]/div/div[2]/div[3]/div/div/div[1]/div[1]/div[3]/a[1]/button'''

    try:
        hyperSel.selenium_utilities.click_button(driver, dossier_xpath)
        time.sleep(3)
        data = got_inside_yellow_button_click(driver)
        return data
    except Exception as e:
        hyperSel.colors_utilities.c_print(f"single_dossier_iterati ERROR", "red")
        hyperSel.colors_utilities.c_print(f"handle_url ERROR", "red")
        print("RETURN FALSE")
        return False

# Main function to iterate over URLs and call the dispatcher
def got_inside_yellow_button_click(driver):
    urls = get_all_head_sliders(driver)  # This should return your list of URLs
    all_data = []
    starting_url_index = 0
    for url in urls[starting_url_index:]:
        #print('11111111url:', url)
        '''TESTING
        if "ruimtes".lower() in url.lower():
            print("GOT THE ruimtes URL")
            data = handle_url(driver, url)
            # hyperSel.log_utilities.log_function(data)
            custom_log.log_to_file(data)
            input("IN THE ruimtes")
        else:
            continue
        '''
        
        
        try:
            data = handle_url(driver, url)
            all_data.append(data)
        except Exception as e:
            print("URL FIALED:", url)
            print(e)
            # input("WHAT WENT WRONG?")

        #if starting_url_index != 0:
        #    print("ONLY DOING ONE ITER, BRAK")
        #    break

    return all_data

def get_all_individual_building_data(driver, building_url):
    # hyperSel.log_utilities.checkpoint()

    hyperSel.selenium_utilities.go_to_site(driver, building_url)

    time.sleep(2)

    question_xpath = ".//div[contains(@class, 'question') and contains(@class, 'flex') and contains(@class, 'items-center')]"

    questions = hyperSel.selenium_utilities.select_multiple_elements_by_xpath(driver, question_xpath)
    for i in questions:
        try:
            xpath = '/html/body/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[1]/div[5]/aside/div[1]/div/div[1]/div[2]/div/div[2]/div/button'
            hyperSel.selenium_utilities.click_button(driver, xpath=xpath, time=0.01)
            # print("WEIRD THING APPEARED")
            time.sleep(0.001)
        except Exception as e:
            pass

        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", i)
        except Exception as e:
            print(1)
            print(e)
        
        try:
            i.click()
            time.sleep(0.1)
        except Exception as e:
            print(2)
            print(e)


    time.sleep(2)
    full_soup = hyperSel.selenium_utilities.get_driver_soup(driver)
    questions_data = extract_question_data(full_soup)

    return questions_data

def get_all_head_sliders(driver):
    soup = hyperSel.selenium_utilities.get_driver_soup(driver)
    urls = []
    all_tags = soup.find_all("a", class_="v-tab")
    for tag in all_tags:
        urls.append(f"https://productie.deatabix.nl{tag['href']}")
    return urls

def gebouwen_scrape(driver, url):
    print("\nExecuting Gebouwen scrape [BUILDINGS]")
    hyperSel.selenium_utilities.go_to_site(driver, url)
    time.sleep(2)

    soup = hyperSel.selenium_utilities.get_driver_soup(driver)

    # GET THE DIV THE BUILDINGS WOULD BE IN
    # print("\n")
    root_building_tag = soup.find("div", class_="atabix-side-menu-draggable__items")
    # print("root_building_tag;", len(root_building_tag))

    if len(root_building_tag) == 0:
        print("NO BUILDINGS HERE, RETURN EMPTY ARR")
        return  []

    all_building_data = []
    for building in root_building_tag:
        try:
            xpath = '/html/body/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[1]/div[5]/aside/div[1]/div/div[1]/div[2]/div/div[2]/div/button'
            hyperSel.selenium_utilities.click_button(driver, xpath=xpath, time=0.0001)
            # print("WEIRD THING APPEARED")
            time.sleep(0.01)
        except Exception as e:
            pass

        try:
            building_title = building.find("span", class_="atabix-side-menu-draggable__item--title").text
        except Exception as e:
            hyperSel.colors_utilities.c_print("FAILED TO GET BUILDING TITLE")
            building_title = ""

        #print("\nbuilding_title:", building_title)

        building_url = f"https://productie.deatabix.nl{building.find('a')['href']}" 
        #print("building_url:", building_url)
        
        questions_data = get_all_individual_building_data(driver, building_url)

        hyperSel.selenium_utilities.go_to_site(driver, building_url+'afbeeldingen')
        time.sleep(3)
        soup = hyperSel.selenium_utilities.get_driver_soup(driver)
        images = extract_image_urls(soup)

        full_object = {
            "building_title":building_title,
            "building_url":building_url,
            "questions_data":questions_data,
            "images":images
        }
        all_building_data.append(full_object)
        
        #print("WENT TO BUILDING URL")
        #print("===="*3)
        time.sleep(3)

    return all_building_data

def extract_image_urls(soup):
    image_urls = []

    # Find all img tags and extract the src attribute
    for img_tag in soup.find_all("img"):
        img_url = img_tag.get("src")
        if img_url:
            image_urls.append(img_url)

    return image_urls

# Dispatcher function to handle different URLs
def handle_url(driver, url):
    if "algemeen" in url:
        data = algemeen_scrape(driver, url)
        tab_type = "algemeen"

    elif "omgevingskenmerken" in url:
        data = omgevingskenmerken_scrape(driver, url)
        tab_type = "omgevingskenmerken"
        
    elif "gebouwen" in url:
        tab_type = "gebouwen"
        data = gebouwen_scrape(driver, url)

    elif "ruimtes" in url:
        tab_type = "ruimtes"
        data = ruimtes_scrape(driver, url)
        
    elif "schades" in url:
        tab_type = "schades"
        data = schades_scrape(driver, url)
    
    elif "bijlagen" in url:
        data = bijlagen_scrape(driver, url)
        tab_type = "bijlagen"
 
    elif "samenvatting" in url:
        data = samenvatting_scrape(driver, url)
        tab_type = "samenvatting"
    try:
        full_data = {
            'data':data,
            'url':url,
            'tab_type':tab_type
        }
        return full_data
    except Exception as e:
        hyperSel.colors_utilities.c_print(f"handle_url ERROR", "red")
        print(url)
        # input("GOOBER mess UP")


def extract_numeric_answers(soup):
    """
    Extract questions with numeric answers from a BeautifulSoup object.

    Args:
        soup (BeautifulSoup): The parsed HTML soup.

    Returns:
        list: A list of dictionaries, each containing a question and its numeric answer.
    """
    question_divs = soup.find_all('div', {'label': True, 'value': True})
    all_questions = []

    for div in question_divs:
        question_name = div.get('label')  # Extract the question text
        radio_button_status = div.get('value')  # Extract the answer

        # Check if the answer is numeric (handles integers and floats)
        try:
            # Attempt to convert the value to a float
            numeric_value = float(radio_button_status)
            all_questions.append({
                "question": question_name,
                "answers": f"{numeric_value}"  # Store the numeric value as a string
            })
        except ValueError:
            # If not numeric, skip or handle as needed
            # print(f"Non-numeric value encountered: {radio_button_status}")
            pass
    
    return all_questions

def extract_questions_without_data(soup):
    """Extract questions from divs with class 'atabix__label-container' that don't have answers."""
    questions_found_without_data = []
    for div in soup.find_all('div', class_="atabix__label-container"):
        if div.text.strip():
            questions_found_without_data.append(div.text.strip())
    return questions_found_without_data


def extract_label_questions_with_answers(soup):
    """Extract questions and their answers from labels with class 'question__name'."""
    all_questions = []
    question_name_tags = soup.find_all("label", class_="question__name")
    for label in question_name_tags:
        question_name = label.text.strip()
        # Find the next div element (regardless of class) for the answer
        answer_div = label.find_next("div")
        answer_value = answer_div["value"] if answer_div and answer_div.get("value") else ""
        all_questions.append({
            "question": question_name,
            "answer": answer_value,
        })
    return all_questions


def add_questions_without_answers(questions_without_data, numeric_answers, all_questions):
    """Add questions without answers if not found in numeric answers."""
    for question_name in questions_without_data:
        if not any(question_name == num_answer['question'] for num_answer in numeric_answers):
            all_questions.append({
                "question": question_name,
                "answer": ""
            })
    return all_questions


def extract_exclusive_radio_button_answers(soup):
    """Extract questions and their radio button options."""
    all_radio_answers = []
    for tag in soup.find_all("span", class_="question__name"):
        question_name = tag.text.strip()
        parent_div = tag.find_parent("div")
        if not parent_div:
            continue

        # Get the next sibling `div` containing the radio button answers
        answer_div = parent_div.find_next_sibling("div")
        if not answer_div:
            continue

        # Collect radio button statuses
        radio_button_status = {}
        for container in answer_div.find_all("div", class_="radio-input-container"):
            label_tag = container.find("label")
            input_tag = container.find("input", type="radio")
            if label_tag and input_tag:
                label = label_tag.text.strip()
                is_selected = input_tag.get("aria-checked") == "true"
                radio_button_status[label] = is_selected

        if radio_button_status:
            all_radio_answers.append({
                "question": question_name,
                "answers": radio_button_status
            })
    return all_radio_answers


def extract_question_data(soup, verbose=False):
    
    # hyperSel.log_utilities.log_function(soup)


    """Main function to orchestrate question and answer extraction."""
    all_questions = []

    # Extract questions without data
    questions_found_without_data = extract_questions_without_data(soup)
    if verbose:
        print("questions_found_without_data", len(questions_found_without_data))
        
        #for i in questions_found_without_data:
        #    print(i)

    # Extract label-based questions with answers
    label_questions = extract_label_questions_with_answers(soup)
    if verbose:
        print("label_questions", len(label_questions))
        for i in label_questions:
            print(i)
    all_questions.extend(label_questions)


    # Extract numeric answers
    numeric_answers = extract_numeric_answers(soup)
    if verbose:
        print("numeric_answers", len(numeric_answers))
        for i in numeric_answers:
            print(i)
    all_questions.extend(numeric_answers)

    # Add questions without data
    all_questions = add_questions_without_answers(
        questions_found_without_data, numeric_answers, all_questions
    )
    if verbose:
        print("questions_without_answers", len(all_questions))
        for i in all_questions:
            print(i)

    # Extract radio button answers
    radio_button_answers = extract_exclusive_radio_button_answers(soup)
    if verbose:
        print("radio_button_answers", len(radio_button_answers))
    all_questions.extend(radio_button_answers)

    # Extract radio button answers2
    exlusive_radio_buttons =  extract_inclusive_radio_button_answers(soup)
    if verbose:
        print("exlusive_radio_buttons", len(exlusive_radio_buttons))
    all_questions.extend(exlusive_radio_buttons)

    return all_questions

def extract_inclusive_radio_button_answers(soup):
    """Extract inclusive radio button answers (checkboxes) for questions."""
    all_radio_answers = []

    # Find all questions
    for tag in soup.find_all("span", class_="question__name"):
        question_name = tag.text.strip()

        # Move to the parent div to locate the checkbox group
        parent_div = tag.find_parent("div")
        if not parent_div:
            continue

        # Get the next sibling div containing the checkbox answers
        answer_div = parent_div.find_next_sibling("div")
        if not answer_div:
            continue

        # Collect checkbox statuses
        checkbox_status = {}
        for container in answer_div.find_all("div", class_="flex"):
            # Extract the label and the selection status
            label = container.get("label", "").strip()
            input_tag = container.find("input", type="checkbox")
            if label and input_tag:
                is_checked = input_tag.get("aria-checked") == "true"
                checkbox_status[label] = is_checked

        # If no checkboxes were found, skip this question
        if not checkbox_status:
            continue

        # Append the question and its answers to the result
        all_radio_answers.append({
            "question": question_name,
            "answers": checkbox_status
        })

    return all_radio_answers

def ruimtes_scrape(driver, url):
    print("\nExecuting Ruimtes scrape")
    hyperSel.selenium_utilities.go_to_site(driver, url)
    time.sleep(2)
    
    class_name = 'atabix-side-menu-draggable__item'
    spaces = hyperSel.selenium_utilities.select_multiple_elements_by_class(driver, class_name=class_name)
    # print("spaces", len(spaces))
    if len(spaces) == 0:
        return []
    
    all_space_data = []

    for i in spaces:
        try:
            xpath = '/html/body/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[1]/div[5]/aside/div[1]/div/div[1]/div[2]/div/div[2]/div/button'
            hyperSel.selenium_utilities.click_button(driver, xpath=xpath, time=0.0001)
            # print("WEIRD THING APPEARED")
            time.sleep(0.01)
        except Exception as e:
            pass

        # print("[1]1[]1[]1[]i:", i)
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", i)
            time.sleep(0.01)
        except Exception as e:
            print(1)
            print(e)

        for l in range(5):   
            try:
                i.click()
                time.sleep(0.01)
            except Exception as e:
                print(2)
                print(e)

        try:
            xpath = '/html/body/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[1]/div[5]/aside/div[1]/div/div[1]/div[2]/div/div[2]/div/button'
            hyperSel.selenium_utilities.click_button(driver, xpath=xpath, time=0.0001)
            # print("WEIRD THING APPEARED")
            time.sleep(0.001)
        except Exception as e:
            pass

        time.sleep(2)

        data = get_individual_space_data_after_click(driver)
        #custom_log.log_to_file(data)
        all_space_data.append(data)

        # print(data)
        # custom_log.log_to_file(data)
        # input("SINGLE SPACE CHECK")
        # hyperSel.log_utilities.checkpoint()
        time.sleep(1)
        # print("======"
        #input("DID A SINGLE SPACE?")

    #custom_log.log_to_file(all_space_data)
    #input("DONE A WHOLE SPACE")
    return all_space_data

def get_individual_space_data_after_click(driver):
    soup = hyperSel.selenium_utilities.get_driver_soup(driver)
    full_object = {}

    images = extract_image_urls(soup)
    full_object['images'] = images
    # print("images:", images)

    space_title = soup.find("h2",class_="atabix-title").text
    # print("space_title:", space_title)
    full_object['title'] = space_title

    try:
        question_xpath = ".//div[contains(@class, 'question') and contains(@class, 'flex') and contains(@class, 'items-center')]"

        questions = hyperSel.selenium_utilities.select_multiple_elements_by_xpath(driver, question_xpath)

        for element in questions:
            try:
                driver.execute_script("arguments[0].scrollIntoView(true);", element)
                element.click()
                time.sleep(0.2)
            except Exception as e:
                pass
            
            try:
                xpath = '/html/body/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[1]/div[5]/aside/div[1]/div/div[1]/div[2]/div/div[2]/div/button'
                hyperSel.selenium_utilities.click_button(driver, xpath=xpath, time=0.0001)
                time.sleep(0.01)
            except Exception as e:
                pass
                
        time.sleep(2)
        soup = hyperSel.selenium_utilities.get_driver_soup(driver)
        # hyperSel.log_utilities.log_function(soup)
        questionaaire_data = extract_question_data(soup)
        full_object["questionaire_data"] = questionaaire_data

    except Exception as e:
        print(e)

    return full_object    

def schades_scrape(driver, url):
    print("\nExecuting Schades scrape")
    hyperSel.selenium_utilities.go_to_site(driver, url)
    time.sleep(2)

    class_name = 'atabix-side-menu-draggable__item'
    damages = hyperSel.selenium_utilities.select_multiple_elements_by_class(driver, class_name=class_name)
    print("damages", len(damages))
    if len(damages) == 0:
        return []
    
    all_damages = []

    for i in damages:
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", i)
        except Exception as e:
            print(1)
            print(e)

        try:
            i.click()
            
        except Exception as e:
            print(2)
            print(e)
        
        time.sleep(2.5)

        try:
            xpath = '/html/body/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[1]/div[5]/aside/div[1]/div/div[1]/div[2]/div/div[2]/div/button'
            hyperSel.selenium_utilities.click_button(driver, xpath=xpath, time=0.0001)
            # print("WEIRD THING APPEARED")
            time.sleep(0.01)
        except Exception as e:
            pass

        full_object = get_individual_space_data_after_click(driver)
        all_damages.append(full_object)

    return all_damages

def bijlagen_scrape(driver, url):
    print("\nExecuting Bijlagen scrape")
    hyperSel.selenium_utilities.go_to_site(driver, url)
    time.sleep(2)
    # print("ATTACHMENTS IS WEIRD")
    return [ ]

def samenvatting_scrape(driver, url):
    print("\nExecuting Samenvatting scrape")
    hyperSel.selenium_utilities.go_to_site(driver, url)
    time.sleep(5)
    soup = hyperSel.selenium_utilities.get_driver_soup(driver)
    # hyperSel.log_utilities.log_function(soup)

    data = {}
    section_soup = soup.find("div", class_="conclusion-card-content")
    for item in section_soup.find_all("div", class_="label-value"):
        # Extract label text
        label = item.find("div", class_="label-value__label").text.strip()
        
        # Extract value text
        value = item.find("div", class_="label-value__value").text.strip()
        
        # Add to dictionary
        data[label] = value

    if data == {}:
        # input("EMPTY SAMEN DATA")
        pass

    return data

def algemeen_scrape(driver, url):
    try:
        print("\nExecuting Algemeen scrape")
        hyperSel.selenium_utilities.go_to_site(driver, url)
        time.sleep(2)
        hyperSel.selenium_utilities.default_scroll_to_buttom(driver)

        for i in range(0, 10):# 100 IS OVERKILL but just gets em all
            try:
                #         /html/body/div/div[1]/div/div[2]/div[2]/div[2]/div/div/div/div[1]
                xpath = f'/html/body/div/div[1]/div/div[2]/div[2]/div[2]/div/div/div/div[{i}]/div'
                # /html/body/div/div[1]/div/div[2]/div[2]/div[2]/div/div/div/div[6]
                
                hyperSel.selenium_utilities.click_button(driver, xpath, time=0.001)
                # hyperSel.colors_utilities.c_print(i, "blue")
            except Exception as e:
                # hyperSel.colors_utilities.c_print(i, "red")
                pass
            finally:
                time.sleep(2)
                continue

        # print("DONE HERE")
        soup = hyperSel.selenium_utilities.get_driver_soup(driver)

        question_soups = soup.find_all("div", class_="question relative")
        all_questions = []
        for question_tag in question_soups:
            try:
                # print("question_tag:", question_tag)
        
                # results 
                radio_button_status = {}
                # print(1)
                # Find all radio button containers and extract label and selection status
                for container in question_tag.find_all("div", class_="radio-input-container"):
                    # print(2)
                    # Get the label text
                    label = container.find("label").text.strip()
                    
                    # Get the selection status from 'aria-checked' attribute in the input tag
                    input_tag = container.find("input", type="radio")
                    is_selected = input_tag.get("aria-checked") == "true"
                    
                    # Add to dictionary
                    radio_button_status[label] = is_selected

                # print("radio_button_status:", radio_button_status)

                if radio_button_status == {}:
                    continue

                question_name = question_tag.find("span", class_="question__name").text
                # print("\nquestion", question_name)

                # print("=====\n\n")
                full_object = {
                    "question": question_name,
                    "answers": radio_button_status
                }
                all_questions.append(full_object)
            except Exception as e:
                hyperSel.colors_utilities.c_print("internal break of some kind", "green")
            
    except Exception as e:
        hyperSel.colors_utilities.c_print(f"algemeen_scrap ERROR", "red")
        print(e)
        
        # input("SINGLE STOPPAGE")

    return all_questions


def omgevingskenmerken_scrape(driver, url):
    print("\nomgevingskenmerken_scrape")
    try:
        hyperSel.selenium_utilities.go_to_site(driver, url)
        time.sleep(4)
        hyperSel.selenium_utilities.default_scroll_to_buttom(driver)

        for i in range(0, 10):# 100 IS OVERKILL but just gets em all
            try:
                #         /html/body/div/div[1]/div/div[2]/div[2]/div[2]/div/div/div/div[1]
                xpath = f'/html/body/div/div[1]/div/div[2]/div[2]/div[2]/div/div/div/div[{i}]/div'
                # /html/body/div/div[1]/div/div[2]/div[2]/div[2]/div/div/div/div[6]
                
                hyperSel.selenium_utilities.click_button(driver, xpath, time=0.001)
                # hyperSel.colors_utilities.c_print(i, "blue")
            except Exception as e:
                # hyperSel.colors_utilities.c_print(i, "red")
                pass
            finally:
                time.sleep(2)
                continue

        # print("DONE HERE")
        soup = hyperSel.selenium_utilities.get_driver_soup(driver)

        question_soups = soup.find_all("div", class_="question relative")
        all_questions = []
        for question_tag in question_soups:
            try:
                # print("question_tag:", question_tag)
        
                # results 
                radio_button_status = {}
                # print(1)
                # Find all radio button containers and extract label and selection status
                for container in question_tag.find_all("div", class_="radio-input-container"):
                    # print(2)
                    # Get the label text
                    label = container.find("label").text.strip()
                    
                    # Get the selection status from 'aria-checked' attribute in the input tag
                    input_tag = container.find("input", type="radio")
                    is_selected = input_tag.get("aria-checked") == "true"
                    
                    # Add to dictionary
                    radio_button_status[label] = is_selected

                # print("radio_button_status:", radio_button_status)

                if radio_button_status == {}:
                    continue

                question_name = question_tag.find("span", class_="question__name").text
                # print("\nquestion", question_name)

                # print("=====\n\n")
                full_object = {
                    "question": question_name,
                    "answers": radio_button_status
                }

                all_questions.append(full_object)
            except Exception as e:
                hyperSel.colors_utilities.c_print("internal break of some kind", "green")
            
    except Exception as e:
        print(e)
        hyperSel.colors_utilities.c_print(f"mgevingskenmerke ERROR", "red")
        # input("SINGLE STOPPAGE")

    return all_questions

if __name__ == '__main__':
    soup = hyperSel.log_utilities.load_file_as_soup("./logs/2024/12/03/2024-12-03.txt")
    questionaaire_data = extract_question_data(soup, verbose=True)
    custom_log.log_to_file(questionaaire_data)