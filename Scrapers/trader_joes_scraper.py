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
driver.get("https://locations.traderjoes.com/")
chain = {"name": "Trader Joe's", "stores": []}
default_delay = 0.5


def get_list():
    return driver.find_elements_by_class_name("ga_w2gi_lp")


def move(element):
    ActionChains(driver).move_to_element(element).perform()


def scrape(location):
    data = location.text.split("\n")

    address = ", ".join(data[1:-3])
    phone = data[-3]
    remote_id = re.sub("[^0-9]", "", data[0])

    store = {"address": address, "phone": phone, "id": remote_id}
    chain["stores"].append(store)
    print("Added", store)


for state_index in range(len(get_list())):
    time.sleep(default_delay)
    states = get_list()
    state = states[state_index]
    move(state)
    state.click()

    for city_index in range(len(get_list())):
        time.sleep(default_delay)
        cities = get_list()
        city = cities[city_index]

        if city.text == "Select a state":
            continue

        move(city)
        city.click()
        time.sleep(default_delay)

        for location in driver.find_elements_by_class_name("itemlist"):
            scrape(location)

        # Go to cities
        driver.back()

    # Go to states
    driver.back()

with open("../Outputs/trader_joes.json", "w") as f:
    json.dump(chain, f, indent=2)
print("Done")
