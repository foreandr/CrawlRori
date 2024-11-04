
import hyperSel
import hyperSel.selenium_utilities
import hyperSel.soup_utilities
import func
import time
import re

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

def foo():
    pass

def iterate_through_items(driver):
    print("\n\niterate_through_items")
    totals_class = 'atabix-table__item-totals'
    soup = hyperSel.selenium_utilities.get_driver_soup(driver)

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

        time.sleep(4)
        print("---")

    hyperSel.selenium_utilities.close_driver(driver)    
    print("DONE")

def main():
    print("\nMAIN")
    driver = func.sign_in()
    time.sleep(5)

    # get content
    iterate_through_items(driver)
    

    input("END MAIN")


if __name__ == '__main__':
    main()
    
