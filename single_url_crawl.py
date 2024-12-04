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


def single_crawler(url):
    try:
        print("URL", url)

        driver = full_sign_in()
        hyperSel.selenium_utilities.go_to_site(driver, url)
        time.sleep(3)

        title = get_title(driver).strip()
        print("title:", title)

        final_data = {}

        if is_s_version(title):
            print("FULL WITH CONTROL TOOL")
            # TRY RECORDING TOOL DATA  
            hyperSel.selenium_utilities.go_to_site(driver, url)
            final_data['recording_tool'] = recording_tool.recording_tool_crawl(driver, url)     
            
            # RESET BACK TO OG PAGE
            hyperSel.selenium_utilities.go_to_site(driver, url)
            final_data['control_tool'] = control_tool.control_tool_crawl(driver, url)
        else:
            hyperSel.selenium_utilities.go_to_site(driver, url)
            print("JUST RECORDING TOOL")   
            final_data['recording_tool'] = recording_tool.recording_tool_crawl(driver, url)

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
    

    
