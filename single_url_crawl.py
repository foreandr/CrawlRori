import hyperSel.log_utilities
import func
import hyperSel
import hyperSel.selenium_utilities
import recording_tool
import time

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

        title = get_title(driver)
        print("title:", title)

        # TRY RECORDING TOOL DATA
        data = recording_tool.recording_tool_crawl(driver, url)
        print("DATA;", data)
        return data
    
        # RESET BACK TO OG PAGE
        hyperSel.selenium_utilities.go_to_site(driver, url)

        # TRY CONTROL TOOL DATA
        #try

        input("WENT TO SITE")
    except Exception as e:
        print("E", e)
        input("E STOP")
    
    return data

if __name__ == '__main__':
    url = 'https://productie.deatabix.nl/dossiers/9d8686f8-8b86-43f2-ae2c-cfb9202d86e1/overzicht'
    data = single_crawler(url=url)

