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
driver.get("https://www.costco.com/WarehouseListByStateDisplayView")
chain = {"name": "Costco", "stores": []}
default_delay = 1.5


def move(element):
    ActionChains(driver).move_to_element(element).perform()


time.sleep(default_delay)
state_buttons = driver.find_elements_by_class_name("warehouse-title-link")
for state_button in state_buttons:

    if state_button.text == "":
        continue

    move(state_button)
    state_button.click()
    time.sleep(default_delay)

    locations = driver.find_elements_by_class_name("warehouse-item")
    for location in locations:
        address = location.find_element_by_class_name(
            "h6-style-guide").text.replace("\n", ", ")
        phone = location.find_element_by_class_name(
            "body-copy-link").text[1:].replace(") ", "-")
        location_url = location.find_element_by_link_text(
            "Store Details").get_attribute("href")
        remote_id = remote_id = re.sub("[^0-9]", "", location_url)

        store = {"address": address, "phone": phone, "id": remote_id}
        chain["stores"].append(store)
        print("Added", store)

with open("../Outputs/costco.json", "w") as f:
    json.dump(chain, f, indent=2)
print("Done")
