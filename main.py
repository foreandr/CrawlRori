
import hyperSel
import hyperSel.colors_utilities
import hyperSel.log_utilities
import hyperSel.selenium_utilities
import hyperSel.soup_utilities
import func
import time
import re
import custom_log
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

print("NEED SOME KIND OF KEY SYSTEM, SO THAT WHEN I SEND THE EXE, ITS JUST FINITE")
def extract_numbers_from_string(text):
    """
    Function to extract all numbers from a given string and return them as a list.
    """
    numbers = re.findall(r'\d+', text)
    return [int(num) for num in numbers]

def any_more_button_clicks(numbers):
    """
    Function that takes a list of numbers and checks if the last two numbers are equal.
    Returns True if they are equal, otherwise False.
    """
    if len(numbers) >= 2 and numbers[-1] == numbers[-2]:
        return False
    return True

def get_content_from_page(driver):
    print("[1]: get_content_from_page")
    soup = hyperSel.selenium_utilities.get_driver_soup(driver)
    # hyperSel.log_utilities.log_function(soup)
    all_tr_tags = soup.find_all("tr")
    all_data = []
    for tag in all_tr_tags:
        data = {}
        
        # Dossier
        tag_str = str(tag)
        dossier_title_pattern = r'[A-Z]+-\d{7}'
        try:
            first_dossier = re.search(dossier_title_pattern, tag_str)
            data["dossier"] = first_dossier.group(0) if first_dossier else None
        except AttributeError:
            data["dossier"] = None
        
        if data['dossier'] == None:
            continue
    
        # Title
        try:
            data["title"] = tag.find("div", class_="atabix-status-indicator pl-0").text
        except AttributeError:
            data["title"] = None

        # Address
        try:
            address = tag.find("a", class_="img-report-address-link").text
            data["address"] = address
        except (IndexError, AttributeError):
            data["address"] = None

        # Dossier link (additional href containing "/dossiers/")
        tag_str = str(tag)
        dossier_pattern = r'/dossiers/[a-f0-9\-]+/overzicht'
        try:
            dossier_url = re.search(dossier_pattern, tag_str)
            single= dossier_url.group(0) if dossier_url else None
            full_url = f"https://productie.deatabix.nl{single}"
            data["dossier_url"] =full_url 
        except AttributeError:
            data["dossier_url"] = None
        if dossier_url == None:
            continue
        all_data.append(data)

    return all_data

def get_all_head_sliders(driver):
    soup = hyperSel.selenium_utilities.get_driver_soup(driver)
    urls = []
    all_tags = soup.find_all("a", class_="v-tab")
    for tag in all_tags:
        urls.append(f"https://productie.deatabix.nl{tag['href']}")
    return urls

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
                    question_name:radio_button_status
                }
                all_questions.append(full_object)
            except Exception as e:
                hyperSel.colors_utilities.c_print("internal break of some kind", "green")
            
    except Exception as e:
        hyperSel.colors_utilities.c_print(f"algemeen_scrap ERROR", "red")
        print(e)
        
        input("SINGLE STOPPAGE")

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
                    question_name:radio_button_status
                }
                all_questions.append(full_object)
            except Exception as e:
                hyperSel.colors_utilities.c_print("internal break of some kind", "green")
            
    except Exception as e:
        print(e)
        hyperSel.colors_utilities.c_print(f"mgevingskenmerke ERROR", "red")
        input("SINGLE STOPPAGE")

    return all_questions

def get_all_individual_building_data(driver, building_url):

    hyperSel.selenium_utilities.go_to_site(driver, building_url)

    time.sleep(2)


    question_xpath = ".//div[contains(@class, 'question') and contains(@class, 'flex') and contains(@class, 'items-center')]"

    questions = hyperSel.selenium_utilities.select_multiple_elements_by_xpath(driver, question_xpath)
    for i in questions:
        try:
            xpath = '/html/body/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[1]/div[5]/aside/div[1]/div/div[1]/div[2]/div/div[2]/div/button'
            hyperSel.selenium_utilities.click_button(driver, xpath=xpath, time=0.0001)
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
        except Exception as e:
            print(2)
            print(e)

        
    time.sleep(2)
    full_soup = hyperSel.selenium_utilities.get_driver_soup(driver)
    questions_data = extract_question_data(full_soup)

    return questions_data

def extract_image_urls(soup):
    image_urls = []

    # Find all img tags and extract the src attribute
    for img_tag in soup.find_all("img"):
        img_url = img_tag.get("src")
        if img_url:
            image_urls.append(img_url)

    return image_urls

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
        #for i in questions_data:
        #    print(i)
        #    print("======")

        # get images
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
            time.sleep(0.001)
        except Exception as e:
            pass

        # print("[1]1[]1[]1[]i:", i)
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", i)
        except Exception as e:
            print(1)
            print(e)


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
        all_space_data.append(data)
        hyperSel.log_utilities.checkpoint()
        time.sleep(1)
        # print("======"

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
        elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@data-v-b8e230b8]"))
        )

        # print("elements:",len(elements))
        # Click each element
        for element in elements:
            try:
                driver.execute_script("arguments[0].scrollIntoView(true);", element)
                element.click()
                time.sleep(0.01)
            except Exception as e:
                #print(1)
                #print(e)
                pass

            try:
                xpath = '/html/body/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[1]/div[5]/aside/div[1]/div/div[1]/div[2]/div/div[2]/div/button'
                hyperSel.selenium_utilities.click_button(driver, xpath=xpath, time=0.0001)
                # print("WEIRD THING APPEARED")
                time.sleep(0.01)
            except Exception as e:
                pass
                
        time.sleep(2)
        soup = hyperSel.selenium_utilities.get_driver_soup(driver)
        questionaaire_data = extract_question_data(soup)
        full_object["questionaire_data"] = questionaaire_data

    except Exception as e:
        print(e)
        input("WHAT THE FUCK")

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
    print("ATTACHMENTS IS WEIRD")
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
        input("EMPTY SAMEN DATA")

    return data

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
        # print("full_data:", full_data)
        return full_data
    except Exception as e:
        hyperSel.colors_utilities.c_print(f"handle_url ERROR", "red")
        print(url)
        input("GOOBER FUCK UP")
        
# Main function to iterate over URLs and call the dispatcher
def got_inside_yellow_button_click(driver):
    urls = get_all_head_sliders(driver)  # This should return your list of URLs
    all_data = []
    starting_url_index = 0
    for url in urls[starting_url_index:]:
        # print('11111111url:', url)
        try:
            # hyperSel.colors_utilities.c_print(text="FOR ANY OF THESE, IF DATA IS NONE, RUN AGAIN TO ATTEMPT, GIVE N ATTEMPTS", color="cyan")
            data = handle_url(driver, url)
            all_data.append(data)
            # print("data:", data)
            # input("I AM TRYING TO DO THE SECOND TAB")
        except Exception as e:
            print("URL FIALED:", url)
            print(e)
            input("WHAT WENT WRONG?")

        if starting_url_index != 0:
            print("ONLY DOING ONE ITER, BRAK")
            break

    return all_data

def single_dossier_iteration(driver):
    # print("single_dossier_iteration")
    dossier_xpath = '''/html/body/div/div[1]/div/div[2]/div[3]/div/div/div[1]/div[1]/div[3]/a[1]/button'''

    try:
        hyperSel.selenium_utilities.click_button(driver, dossier_xpath)
        time.sleep(3)
        data = got_inside_yellow_button_click(driver)
        # print("RETURN TRUESKI:", data)
        return data
    except Exception as e:
        hyperSel.colors_utilities.c_print(f"single_dossier_iterati ERROR", "red")
        hyperSel.colors_utilities.c_print(f"handle_url ERROR", "red")
        print("RETURN FALSE")
        return False
   
def iterate_through_main_data(driver, data):    
    # print("\n[2]: iterate_through_main_data")
    for item in data:
        #NEED TO BE RELOAIDNG THE DATA, CHECK THE SV
        # IF THE SV IS IN THERE, THEN WE just update the values of that sv
        url = item['dossier_url']
        print("url:", url)
        time.sleep(4)

        hyperSel.selenium_utilities.go_to_site(driver, url)
        time.sleep(2)

        tab_data = single_dossier_iteration(driver)
        combined_data = {}
        combined_item = {**item, "tab_data": tab_data}  # Combines all keys in `item` and adds `tab_data`
        combined_item.pop("dossier", None)
        dossier_key = item['dossier']  
        combined_data[dossier_key] = combined_item

        #print("combined_data:", combined_data)
        #print("=====-----"*3)
        custom_log.log_to_file(combined_data, file_path="./logs/crawl_data.json")# hyperSel.log_utilities.log_data(combined_data)

    print("DONE") 

def iterate_through_items(driver):
    print("\n\niterate_through_items")
    totals_class = 'atabix-table__item-totals'
    soup = hyperSel.selenium_utilities.get_driver_soup(driver)

    num_pages_done = 0
    while True:
        totals = hyperSel.soup_utilities.get_text_by_tag_and_class(soup=soup, tag='div', selector_name=totals_class)
        print("total:", totals)

        numbers = extract_numbers_from_string(totals)
        print("numbers:", numbers)

        clicks = any_more_button_clicks(numbers)
        print("clicks:", clicks)

        if clicks == False:
            print("WE HIT THE END STOP")
            break

        all_data = get_content_from_page(driver)
        iterate_through_main_data(driver, all_data)

        print("BACK TO ROOT PAGE")
        print("THEN I HAVE TO PAGINATE N times actually, NTO JUST ONCE SO THIS NEEDS OT BE FIXED")
        site = "https://productie.deatabix.nl/login?redirect=/dashboard"
        hyperSel.selenium_utilities.go_to_site(driver, site)
        time.sleep(2)

        try:
            time.sleep(1)
            elements = hyperSel.selenium_utilities.select_multiple_elements_by_class(driver, "v-pagination__navigation")
            last_button = elements[1]
            driver.execute_script("arguments[0].scrollIntoView(true);", last_button)
            last_button.click()
        except Exception as e:
            hyperSel.colors_utilities.c_print(F"I FAILED TO PAGINATE [{num_pages_done}]", "red")
            print("ISSUE WITH NEXT BUUTTON?")
            print("SIGN IN AGAIN")
            hyperSel.selenium_utilities.close_driver(driver)

            driver = func.sign_in()

        num_pages_done += 1
        hyperSel.colors_utilities.c_print("DONE, GOING TO NEXT PAGE", 'green')

        time.sleep(4)
        print("---")

    hyperSel.selenium_utilities.close_driver(driver)    
    print("DONE")

def main():
    print("\nMAIN")
    driver = func.sign_in()
    print("SIGNED IN")
    time.sleep(5)

    # get content
    iterate_through_items(driver)
    

    # input("END MAIN")

def extract_question_data(soup):
    all_questions = []

    # Loop through each div with class 'flex flex-col'
    for tag in soup.find_all("div", class_="flex flex-col"):
        try:
            # Extract question name
            question_name_tag = tag.find("span", class_="question__name")
            if question_name_tag:
                question_name = question_name_tag.text.strip()
            else:
                continue  # Skip if there's no question name

            # Initialize a dictionary to store answer statuses
            radio_button_status = {}

            # Find all radio button containers within this question's tag
            for container in tag.find_all("div", class_="radio-input-container"):
                # Extract the label and selection status
                label_tag = container.find("label")
                input_tag = container.find("input", type="radio")
                
                # Ensure label and input are found
                if label_tag and input_tag:
                    label = label_tag.text.strip()
                    is_selected = input_tag.get("aria-checked") == "true"
                    # Store in the dictionary
                    radio_button_status[label] = is_selected

            # If no radio buttons were found, skip this question
            if not radio_button_status:
                continue

            # Append question and answers to the result list
            all_questions.append({
                "question": question_name,
                "answers": radio_button_status
            })

        except Exception as e:
            print("Error processing question:", e)

    return all_questions

if __name__ == '__main__':
    main()
