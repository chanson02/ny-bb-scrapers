import json
import time
import pdb
import re
import traceback

from selenium import webdriver

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

from selenium.common import exceptions

chain = {"name": "Dollar Tree", "stores": []}

driver = webdriver.Chrome('../chromedriver.exe')
driver.get("https://www.dollartree.com/locations/")

view = "None"


def scrape():
    data = driver.find_element_by_xpath(
        "//div[@itemprop='address']").text.split("\n")
    address = ", ".join(data[1:-1])
    phone = data[-1]
    remote_id = re.sub("[^0-9]", "", data[0])

    store = {"address": address, "phone": phone, "id": remote_id}
    chain["stores"].append(store)
    print("Added", store)


def move(element):
    ActionChains(driver).move_to_element(element).perform()


def get_list(element):
    return element.find_elements_by_class_name("ga_w2gi_lp")


state_table_path = '//*[@id="sli_container"]/div[2]/table'
city_table_path = '//*[@id="body_wrap"]/div[2]/table'

state_table = driver.find_element_by_xpath(state_table_path)

# Search states
for state_index in range(len(get_list(state_table))):
    view = "state"
    time.sleep(1)
    state_table = driver.find_element_by_xpath(state_table_path)
    states = get_list(state_table)
    state = states[state_index]
    move(state)
    state.click()

    # Search cities
    city_table = driver.find_element_by_xpath(city_table_path)
    for city_index in range(len(get_list(city_table))):
        view = "city"
        time.sleep(1)
        city_table = driver.find_element_by_xpath(city_table_path)
        cities = get_list(city_table)
        city = cities[city_index]
        move(city)
        city.click()

        # Search locations
        locations = driver.find_elements_by_class_name("storeinfo_div")
        for loc_index in range(len(locations)):
            view = "locations"
            time.sleep(1)
            locations = driver.find_elements_by_class_name("storeinfo_div")
            location = locations[loc_index]
            move(location)
            location.click()
            view = "store"

            # Scrape loction
            try:
                scrape()
            except Exception:
                pass

            # Go back to location view
            driver.back()

        # Go back to cities view
        driver.back()

    # Go back to states view
    driver.back()


with open("../Outputs/dollar_tree.json", "w") as f:
    json.dump(chain, f, indent=2)
print("Done")
