
import hyperSel
import hyperSel.selenium_utilities
import time
import easyocr
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
from main import main_loop
import json
# Preload EasyOCR model
reader = easyocr.Reader(['en'], gpu=False)  # Set gpu=True if you have a CUDA-compatible GPU and installed drivers

username = "roni@octa-advies.nl"
password = "husba8-sepjut-zyBjov"
img_path = "mfa.png"


def get_element_by_tag(driver, tag_name):
    # NEW FUNCTION!!
    """
    Function to get an element by its tag name and wait until it is clickable.
    """
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.TAG_NAME, tag_name)))
    return element

def extract_text_with_easyocr(image_path):
    """
    Function to extract text from an image using EasyOCR.
    """
    results = reader.readtext(image_path)
    extracted_text = "\n".join([text for _, text, _ in results])
    return extracted_text

def find_mfa_tokens(text):
    """
    Function to find patterns like '545 580' in a given text and return them as MFA tokens.
    """
    pattern = r'\b\d{3} \d{3}\b'
    matches = re.findall(pattern, text)
    return matches[0]

def click_play(driver):
    time.sleep(2)

    for i in range(10):
        try:
            hyperSel.selenium_utilities.click_button(driver, '''//*[@id="movie_player"]/div[29]/div[2]/div[1]/button''')
            break
        except Exception as e:
            try:
                hyperSel.selenium_utilities.click_button(driver, '''//*[@id="movie_player"]/div[7]/button''')
                break
            except Exception as e:
                print("e1")
            print("e2")

def screenshot(driver, path):
    time.sleep(3)
    hyperSel.selenium_utilities.take_screenshot(driver, file_path=path)# get mfa

def sign_in():
    print("\nSIGN IN")
    try:
        current_url = "https://www.youtube.com/live/kH2jSStTQU8"
        # 1. open driver
        driver = hyperSel.selenium_utilities.open_site_selenium(site=current_url, show_browser=True)
        hyperSel.selenium_utilities.maximize_the_window(driver)
        
        click_play(driver)
        screenshot(driver, img_path)

        for i in range(10):
            print("MFA ATTEMPT", i)
            try:
                start = time.time()
                text_extracts = extract_text_with_easyocr(img_path)
                print("TEXT", time.time()-start)
                mfa = find_mfa_tokens(text_extracts)
                print("mfa:", mfa)
                break
            except Exception as e:
                if i >= 9:
                    hyperSel.selenium_utilities.close_driver(driver)
                    print("MFA FAILURE: I HAD TO DO A LOOP RESET")
                    sign_in()
                continue   

        # print("GOT SCREENSHOT")
        
        site = "https://productie.deatabix.nl/login?redirect=/dashboard"
        hyperSel.selenium_utilities.go_to_site(driver, site)
        time.sleep(2)
        
        username_xpath = '''/html/body/div/div[1]/div/div/div[3]/div/form/div[1]/div/div/div[1]/div[2]/input'''
        hyperSel.selenium_utilities.enter_keys(driver, username_xpath, username)
        
        password_xpath = '''/html/body/div/div[1]/div/div/div[3]/div/form/div[2]/div/div/div[1]/div[2]/input'''
        hyperSel.selenium_utilities.enter_keys(driver, password_xpath, password)
        
        token_xpath = '''//*[@id="input-46"]'''
        hyperSel.selenium_utilities.enter_keys(driver, token_xpath, mfa)

        current_url = driver.current_url

        login_button_xpath = '''/html/body/div/div[1]/div/div/div[3]/div/form/div[4]/button'''
        hyperSel.selenium_utilities.click_button(driver, login_button_xpath)
        time.sleep(3)

        second_url = driver.current_url

        if second_url != current_url:
            print("we in")
            return driver
        else:
            print(current_url)
            print(second_url)
            print("DDINT LOGIN CORRECTLY, PAGE CHANGE FAILED, RESTART")
            hyperSel.selenium_utilities.close_driver(driver)
            sign_in()

    except Exception as e:
        hyperSel.selenium_utilities.close_driver(driver)
        print("I HAD TO DO A GLOBAL RESET")
        sign_in()
    
    return driver

def ui_real_sign_in():
    driver = hyperSel.selenium_utilities.open_site_selenium(site='https://productie.deatabix.nl/login?redirect=/dashboard', show_browser=True)
    hyperSel.selenium_utilities.maximize_the_window(driver)
    print("**"*10)
    options = ['y', 'yes']
    while True:
        
        result = input("\n\nenter y/yes AND PRESS ENTER IF YOU HAVE SIGNED INTO THE SITE\n")
        if result.lower() in options:
            break
    print("**"*10)
    print("USER HAS SIGNED IN, BEGIN CRAWL")
    return driver

def load_json(file_path):
    """
    Loads JSON data from a file.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict or list: Parsed JSON data.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        # print("JSON data loaded successfully.")
        return data
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON. {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    
def get_recording_tool_data(recording_tool_data):
    algemeen_data = None
    omgevingskenmerken_data = None
    gebouwen_data = None
    ruimtes_data = None
    schades_data = None
    bijlagen_data = None
    samenvatting_data = None

    # Loop through recording_tool_data to categorize data by tab_type
    for item in recording_tool_data:
        tab_type = item["tab_type"]
        if tab_type == "algemeen":
            algemeen_data = item
        elif tab_type == "omgevingskenmerken":
            omgevingskenmerken_data = item
        elif tab_type == "gebouwen":
            gebouwen_data = item
        elif tab_type == "ruimtes":
            ruimtes_data = item
        elif tab_type == "schades":
            schades_data = item
        elif tab_type == "bijlagen":
            bijlagen_data = item
        elif tab_type == "samenvatting":
            samenvatting_data = item


    return algemeen_data, omgevingskenmerken_data, gebouwen_data, ruimtes_data, schades_data, bijlagen_data, samenvatting_data