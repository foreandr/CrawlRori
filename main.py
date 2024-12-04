
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

TEST=True

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
            # print("SIGN IN AGAIN")
            hyperSel.selenium_utilities.close_driver(driver)

            # driver = func.sign_in()

        num_pages_done += 1
        hyperSel.colors_utilities.c_print("DONE, GOING TO NEXT PAGE", 'green')

        time.sleep(4)
        print("---")

    hyperSel.selenium_utilities.close_driver(driver)    
    print("DONE")

def full_sign_in():
    if TEST:
        driver = func.sign_in()
    else:
        driver = func.ui_real_sign_in()
    return driver

def main_loop():
    print("\nMAIN")
    print("TEST:", TEST)

    print("SIGNED IN")
    time.sleep(5)

    driver = full_sign_in()
    iterate_through_items(driver)
    # get_single_data_from_url(driver, url)
    
def main_single(url):
    print("url:", url)
    driver = full_sign_in()
    

    input("DOING MAIN SINGLE")
    # https://productie.deatabix.nl/dossiers/9d3c20bc-c2a9-4818-a1aa-5e6efe82f501/overzicht


if __name__ == '__main__':
    url = 'https://productie.deatabix.nl/dossiers/9d3c20bc-c2a9-4818-a1aa-5e6efe82f501/overzicht'
    main_single(url)
