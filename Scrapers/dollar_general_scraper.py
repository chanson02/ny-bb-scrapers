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
driver.get("https://stores.dollargeneral.com/")
chain = {"name": "Dollar General", "stores": []}


def get_list(element):
    return element.find_elements_by_class_name("ga_w2gi_lp")


def move(element):
    ActionChains(driver).move_to_element(element).perform()


def scrape(location):
    data = location.text.split("\n")
    address = ", ".join(data[1:-2])
    phone = data[-2][8:].replace(") ", "-")
    remote_id = re.sub("[^0-9]", "", data[0])

    store = {"address": address, "phone": phone, "id": remote_id}
    chain["stores"].append(store)
    print("Added", store)


for state_index in range(len(get_list(driver))):
    states = get_list(driver)
    state = states[state_index]
    move(state)
    state.click()

    table = driver.find_element_by_class_name("state_wrapper")
    for city_index in range(len(get_list(table))):
        table = driver.find_element_by_class_name("state_wrapper")
        cities = get_list(table)
        city = cities[city_index]
        move(city)
        city.click()

        for location in driver.find_elements_by_class_name("itemlist"):
            scrape(location)

        # Back to cities view
        driver.back()

    # Back to states view
    driver.back()

with open("../Outputs/dollar_general.json", "w") as f:
    json.dump(chain, f, indent=2)
print("Done")
