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
driver.get("https://www.thefreshmarket.com/your-market/store-locator")
chain = {"name": "The Fresh Market", "stores": []}
default_delay = 0.5


def move(element):
    ActionChains(driver).move_to_element(element).perform()


states = driver.find_elements_by_class_name("accordion__item-title")

for state_index in range(len(states)):
    time.sleep(default_delay)
    states = driver.find_elements_by_class_name("accordion__item-title")
    state = states[state_index]
    move(state)
    state.click()
    time.sleep(default_delay)

    links = driver.find_elements_by_class_name(
        "store-list-item-goto-details-link")
    for link_index in range(len(links)):
        time.sleep(default_delay)
        links = driver.find_elements_by_class_name(
            "store-list-item-goto-details-link")
        link = links[link_index]
        move(link)
        link.click()
        time.sleep(default_delay)

        address = ", ".join(driver.find_element_by_class_name(
            "store-detail-overlay-group").text.split("\n")[:-1])
        phone = driver.find_element_by_class_name("simple-link").text
        remote_id = phone.replace("-", "")

        store = {"address": address, "phone": phone, "id": remote_id}
        chain["stores"].append(store)
        print("Added", store)

        # Go back to that same states directory
        driver.back()
        time.sleep(default_delay)
        states = driver.find_elements_by_class_name("accordion__item-title")
        state = states[state_index]
        move(state)
        state.click()

with open("../Outputs/fresh_market.json", "w") as f:
    json.dump(chain, f, indent=2)
print("Done")
