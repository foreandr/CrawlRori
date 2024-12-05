import hyperSel.log_utilities
import func
import hyperSel
import hyperSel.selenium_utilities
import recording_tool
import time
import custom_log
import control_tool

TEST=True

def full_sign_in():
    if TEST:
        driver = func.sign_in()
    else:
        driver = func.ui_real_sign_in()
    return driver

def get_title(driver):
    soup = hyperSel.selenium_utilities.get_driver_soup(driver)
    title = soup.find("h2", class_="atabix-title").text
    return title


def click_recording_tool():
    try:
        pass
    except Exception as e:
        print("FAILED TO CLICK RECORDING TOOL SKIP")
        return False

def click_control_tool():
    try:
        pass
    except Exception as e:
        print("FAILED TO CLICK RECORDING TOOL SKIP")
        return False

def get_button_xpaths(driver):
    from selenium.webdriver.common.by import By
    """
    Extracts the XPaths of all buttons on the current webpage using an existing WebDriver instance.

    Args:
        driver (webdriver): An active Selenium WebDriver instance, already navigated to the desired page.

    Returns:
        list: A list of XPaths for all buttons on the page.
    """
    # Find all buttons on the page
    buttons = driver.find_elements(By.TAG_NAME, "button")

    # Extract the absolute XPaths of all buttons
    button_xpaths = []
    for button in buttons:
        try:
            xpath = driver.execute_script(
                "function absoluteXPath(element) {" 
                "    var path = '';" 
                "    for (; element && element.nodeType === 1; element = element.parentNode) {" 
                "        var index = 0;" 
                "        for (var sibling = element.previousSibling; sibling; sibling = sibling.previousSibling) {" 
                "            if (sibling.nodeType === Node.ELEMENT_NODE && sibling.nodeName === element.nodeName) {" 
                "                index++;" 
                "            }" 
                "        }" 
                "        var tagName = element.nodeName.toLowerCase();" 
                "        var part = '/' + tagName + (index > 0 ? '[' + (index + 1) + ']' : '');" 
                "        path = part + path;" 
                "    }" 
                "    return path;" 
                "}" 
                "return absoluteXPath(arguments[0]);", 
                button)
            button_xpaths.append(xpath)
        except Exception as e:
            print(f"Could not generate XPath for a button: {e}")

    return button_xpaths


def single_crawler(url):
    try:
        print("URL", url)

        driver = full_sign_in()
        hyperSel.selenium_utilities.go_to_site(driver, url)
        time.sleep(3)

        title = get_title(driver).strip()
        print("title:", title)

        final_data = {}

        # TRY CLICK RECORDING TOOL BUTTON
        try:                
            #                  
            dossier_xpath = '''/html/body/div/div[1]/div/div[2]/div[3]/div/div/div[1]/div[1]/div[3]/a[1]/button'''
            hyperSel.selenium_utilities.click_button(driver, dossier_xpath)
            time.sleep(5)
            final_data['recording_tool'] = recording_tool.got_inside_yellow_button_click(driver)
        except Exception as  e:
            print("FAILED TO CLICK RECORDING TOOL BUTTON")
            final_data['recording_tool'] = []

        hyperSel.selenium_utilities.go_to_site(driver, url)

        # TRY CLICK CONTROL TOOL BUTTON
        try:                                
            dossier_xpath = '''/html/body/div/div[1]/div/div[2]/div[3]/div/div/div[1]/div[1]/div[3]/a[2]/button'''
            hyperSel.selenium_utilities.click_button(driver, dossier_xpath)
            time.sleep(5)
            final_data['control_tool'] = control_tool.control_tool_crawl(driver, url)
        except Exception as  e:
            print("FAILED TO CLICK control TOOL BUTTON")
            final_data['control_tool'] = []
    except Exception as e:
        print("E", e)
        input("E STOP")

    return final_data

def is_s_version(title):
    """
    Checks if the given string starts with 'S-' (case-sensitive).
    
    Args:
        title (str): The title to check.

    Returns:
        bool: True if the title starts with 'S-', otherwise False.
    """
    return title.startswith("S-")

def t1():
    test_titles = [
        "S-4002145 | V1",  # True
        "S-4862205 | V1",  # True
        "SV-1437124 | V1", # False
        "SV-1423102 | V1", # False
        "FS-1004 | V1",    # False
        "S-1476001 | V1",  # True
        "S-1468023 | V1",  # True
        "R-12345 | V2",    # False
    ]

    # Test the function
    for title in test_titles:
        print(f"{title}: {is_s_version(title)}")

if __name__ == '__main__':
    start= time.time()
    url = 'https://productie.deatabix.nl/dossiers/9d78eecd-2f56-4ba3-a7b6-2482ed8ab37e/overzicht'
    data = single_crawler(url=url)
    hyperSel.log_utilities.log_function(data)
    custom_log.log_to_file(data)
    print("DONE IN", time.time()-start)
    print("OUT OF THE FUNCTION")
    

    
