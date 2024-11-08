
import hyperSel
import hyperSel.colors_utilities
import hyperSel.log_utilities
import hyperSel.selenium_utilities
import hyperSel.soup_utilities
import func
import time
import re

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
        # print("\nExecuting Algemeen scrape")
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
        print(e)
        input("SINGLE STOPPAGE")

    '''
    print("FULL OBJECTS")
    for item in all_questions:
        for key,value in item.items():
            print("key  :", key)
            print("value:", value)
    '''

    return all_questions
    # hyperSel.log_utilities.log_data(all_questions)
    # print("")
    # input("WE JUST DOINGT HIS algemeen_scrap ONE")

def omgevingskenmerken_scrape(driver, url):
    print("\nExecuting Omgevingskenmerken scrape")
    hyperSel.selenium_utilities.go_to_site(driver, url)
    # Add your scraping logic for Omgevingskenmerken here
    # driver.get(...)

def gebouwen_scrape(driver, url):
    print("\nExecuting Gebouwen scrape")
    hyperSel.selenium_utilities.go_to_site(driver, url)
    # Add your scraping logic for Gebouwen here
    # driver.get(...)

def ruimtes_scrape(driver, url):
    print("\nExecuting Ruimtes scrape")
    hyperSel.selenium_utilities.go_to_site(driver, url)
    # Add your scraping logic for Ruimtes here
    # driver.get(...)

def schades_scrape(driver, url):
    print("\nExecuting Schades scrape")
    hyperSel.selenium_utilities.go_to_site(driver, url)
    # Add your scraping logic for Schades here
    # driver.get(...)

def bijlagen_scrape(driver, url):
    print("\nExecuting Bijlagen scrape")
    hyperSel.selenium_utilities.go_to_site(driver, url)
    # Add your scraping logic for Bijlagen here
    # driver.get(...)

def samenvatting_scrape(driver, url):
    print("\nExecuting Samenvatting scrape")
    hyperSel.selenium_utilities.go_to_site(driver, url)
    # Add your scraping logic for Samenvatting here
    # driver.get(...)

# Dispatcher function to handle different URLs
def handle_url(driver, url):
    if "algemeen" in url:
        return algemeen_scrape(driver, url)
    elif "omgevingskenmerken" in url:
        omgevingskenmerken_scrape(driver, url)
    elif "gebouwen" in url:
        gebouwen_scrape(driver, url)
    elif "ruimtes" in url:
        ruimtes_scrape(driver, url)
    elif "schades" in url:
        schades_scrape(driver, url)
    elif "bijlagen" in url:
        bijlagen_scrape(driver, url)
    elif "samenvatting" in url:
        samenvatting_scrape(driver, url)
    else:
        print("No matching function for this URL:", url)

# Main function to iterate over URLs and call the dispatcher
def got_inside_yellow_button_click(driver):
    urls = get_all_head_sliders(driver)  # This should return your list of URLs
    all_data = []
    for url in urls:
        # print("HANDLING URL", url)
        data = handle_url(driver, url)
        for item in data:
            all_data.append(item)
        hyperSel.colors_utilities.c_print("ONLY DOING FIRST TAB", color='yellow')
        break
        time.sleep(2)
        print("Processed:", url)
        
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
        # print(e)
        print("RETURN FALSE")
        return False
   
def iterate_through_main_data(driver, data):    
    print("\n[2]: iterate_through_main_data")
    for item in data:
        url = item['dossier_url']
        print("url:", url)
        time.sleep(10)

        hyperSel.selenium_utilities.go_to_site(driver, url)
        local_url_data = single_dossier_iteration(driver)

        combined_data = {}
        combined_item = {**item, "local_url_data": local_url_data}  # Combines all keys in `item` and adds `local_url_data`
        combined_item.pop("dossier", None)
        dossier_key = item['dossier']  
        combined_data[dossier_key] = combined_item

        print("combined_data:", combined_data)
        hyperSel.log_utilities.log_function(log_string=combined_data)
        print("=====-----"*3)
        # print("\n\n\n\n")

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

        try:
            time.sleep(1)
            elements = hyperSel.selenium_utilities.select_multiple_elements_by_class(driver, "v-pagination__navigation")
            last_button = elements[1]
            last_button.click()
        except Exception as e:
            #print("ISSUE WITH NEXT BUUTTON?")
            #print(e)
            #input("STOP")
            break
            
        num_pages_done += 1
    
        input('ONE ITER')

        time.sleep(4)
        print("---")

    input("SSTROPPPP")
    hyperSel.selenium_utilities.close_driver(driver)    
    print("DONE")

def main():
    print("\nMAIN")
    driver = func.sign_in()
    print("SIGNED IN")
    time.sleep(5)

    # get content
    iterate_through_items(driver)
    

    input("END MAIN")


if __name__ == '__main__':
    main()
