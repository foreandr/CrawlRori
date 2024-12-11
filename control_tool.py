import hyperSel
import hyperSel.selenium_utilities
import hyperSel.log_utilities
import hyperSel.colors_utilities
import re
import hyperSel.soup_utilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import custom_log
import time

def control_tool_crawl(driver, url):
    time.sleep(3)

    print("INISDE CONTROL TOOL CRAWLER")
    print("driver:", driver)
    print("url   :", url)
    data = control_tool_logic(driver, url)
    return data

def control_tool_logic(driver, url):
    all_data = {}
    all_data['informatie'] = get_the_informatie_data(driver, url)
    all_data['calculation'] = get_calculation_data(driver, url)
    return all_data

def direct_cost_data(soup):
   # Define headers for the keys
    headers = ["Naam", "Aantal", "Stukprijs", "Staffel", "Ruimte", "Gebouw", "Totaal", "BTW %"]

    # Initialize a list to store extracted rows as dictionaries
    rows = []

    # Iterate through all rows in the table
    for row in soup.find_all("div", class_="costs-conclusion__row"):
        # Extract individual columns in the row
        columns = row.find_all("div", class_="costs-conclusion__item")
        row_data = [col.get_text(strip=True).replace('\xa0', '') for col in columns]
        # print(len(row_data), "row_data:", row_data)

        if len(row_data) == 4:
            # print(f"QUAD: {row_data}")
            # Map QUAD data to a dictionary with most fields empty, except Gebouw
            row_dict = {
                "Naam": row_data[0],
                "Aantal": "",
                "Stukprijs": "",
                "Staffel": "",
                "Ruimte": "",
                "Gebouw": row_data[1],
                "Totaal": "",
                "BTW %": ""
            }
            rows.append(row_dict)

        # Ensure the row has the correct number of columns to match the headers
        if len(row_data) == len(headers):
            # Create a dictionary for the row using headers as keys
            row_dict = dict(zip(headers, row_data))
            rows.append(row_dict)

    return rows

def calculated_data(soup):
    headers = ["Naam", "Aantal","Stukprijs","Subtotaal","Totaal","Cumulatief", "BTW %"]
    # Initialize a list to store extracted rows as dictionaries
    rows = []

    # Iterate through all rows in the table
    for row in soup.find_all("div", class_="costs-conclusion__row"):
        # Extract individual columns in the row
        columns = row.find_all("div", class_="costs-conclusion__item")
        row_data = [col.get_text(strip=True).replace('\xa0', '') for col in columns]
        # print(len(row_data), "row_data:", row_data)

        if len(row_data) == 4:
            # print(f"QUAD: {row_data}")
            # Map QUAD data to a dictionary with most fields empty, except Gebouw
            row_dict = {
                "Naam": row_data[0],
                "Aantal": "",
                "Stukprijs": "",
                "Staffel": "",
                "Ruimte": "",
                "Gebouw": row_data[1],
                "Totaal": "",
                "BTW %": ""
            }
            rows.append(row_dict)

        # Ensure the row has the correct number of columns to match the headers
        if len(row_data) == len(headers):
            # Create a dictionary for the row using headers as keys
            row_dict = dict(zip(headers, row_data))
            rows.append(row_dict)

    return rows

def get_calculation_data(driver, url):
    time.sleep(2)
    print("get_calculation_data")
    control_tool_url = url.replace("overzicht", "editors/controle/beoordelen/calculatie")
    hyperSel.selenium_utilities.go_to_site(driver, control_tool_url)
    time.sleep(10)

    soup = hyperSel.selenium_utilities.get_driver_soup(driver)
    all_calc_data =[ ]
    all_calc_data.extend(direct_cost_data(soup))
    all_calc_data.extend(calculated_data(soup))
    return all_calc_data


def get_the_informatie_data(driver, url):
    print("get_the_informatie_data")
    control_tool_url = url.replace("overzicht", "editors/controle/beoordelen/dossier-informatie")
    hyperSel.selenium_utilities.go_to_site(driver, control_tool_url)
    time.sleep(4)
    soup = hyperSel.selenium_utilities.get_driver_soup(driver)
    data = []
    
    for index, label in enumerate(soup.find_all("div", class_="label-value__label"), start=1):
        label_text = label.text.strip()
        value_div = label.find_next_sibling("div")  # Get the sibling div
        value_text = value_div.get_text(strip=True) if value_div else "No value found"
        
        #print(f"{index}: {label_text}:{value_text}")
        #print("==")
        object = {
            "question":label_text,
            "answers":value_text
        }
        data.append(object)

    return data