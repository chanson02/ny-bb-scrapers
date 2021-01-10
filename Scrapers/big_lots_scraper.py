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

driver = webdriver.Chrome('../chromedriver.exe')
driver.get("https://local.biglots.com/")
chain = {"name": "Big Lots", "stores": []}
default_delay = 0.5


def get_list(element):
    return element.find_elements_by_class_name("Directory-listLink")


def move(element):
    ActionChains(driver).move_to_element(element).perform()


def scrape():
    time.sleep(default_delay)
    address = ", ".join(driver.find_element_by_class_name(
        "c-address").text.split("\n"))
    phone = driver.find_element_by_class_name(
        "Phone-display").text[1:].replace(") ", "-")
    remote_id = re.sub("[^0-9]", "", phone)
    store = {"address": address, "phone": phone, "id": remote_id}
    chain["stores"].append(store)
    print("Added", store)


for state_index in range(len(get_list(driver))):
    time.sleep(default_delay)
    states = get_list(driver)
    state = states[state_index]
    move(state)
    state.click()

    for city_index in range(len(get_list(driver))):
        time.sleep(default_delay)
        cities = get_list(driver)
        city = cities[city_index]
        move(city)
        location_count = int(city.get_attribute("data-count")[1:-1])
        city.click()

        if location_count == 1:
            scrape()
        else:
            for loc_index in range(location_count):
                time.sleep(default_delay)
                locations = driver.find_elements_by_class_name(
                    "Teaser-titleLink")
                location = locations[loc_index]
                move(location)
                location.click()
                time.sleep(default_delay)
                scrape()
                # Back to locations view
                driver.back()

        # Back to cities view
        driver.back()

    # Back to states view
    driver.back()

with open("../Outputs/big_lots.json", "w") as f:
    json.dump(chain, f, indent=2)
print("Done")
