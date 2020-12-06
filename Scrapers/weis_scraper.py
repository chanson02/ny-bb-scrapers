import json
import time
import pdb
import re

from selenium import webdriver

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

from selenium.common import exceptions


chain = {"name": "Weis", "stores": []}

driver = webdriver.Chrome('../chromedriver.exe')
driver.get("https://www.weismarkets.com/stores")
time.sleep(1)

locations = driver.find_elements_by_class_name("store-list__rail")
for location in locations:
    ActionChains(driver).move_to_element(location)
    location.click()
    time.sleep(0.5)
    container = driver.find_element_by_class_name(
        "store-details-pane__scroll-container")
    data = location.find_element_by_class_name(
        "store-preview__info").text.split("\n")

    address = data[4] + ", " + data[5]
    phone = container.find_element_by_class_name(
        "store-details-store-contact__list-item-entry--value").text[1:].replace(") ", "-")
    remote_id = re.sub("[^0-9]", "", data[2])

    store_object = {"address": address, "phone": phone, "id": remote_id}
    chain["stores"].append(store_object)
    print("Added", store_object)

    # Go back to view all
    driver.find_element_by_class_name(
        "store-details-pane__back-button").click()
    time.sleep(0.5)

with open("../Outputs/weis.json", "w") as file:
    json.dump(chain, file, indent=2)
driver.close()
