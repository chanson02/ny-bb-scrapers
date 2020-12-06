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


chain = {"name": "Shop Rite", "stores": []}

driver = webdriver.Chrome('../chromedriver.exe')
driver.get("https://shop.shoprite.com/globaldata/banner-pages/store-locator")

# Select dropdown menu
dropdown = driver.find_element_by_id("Region")
select = Select(dropdown)

search_button = driver.find_element_by_class_name(
    "storeLocatorForm__searchButton")

for state_index in range(len(select.options) - 1):  # -1 for the default

    # Select state and click it
    select.select_by_index(state_index + 1)
    search_button.click()
    time.sleep(2)  # Let it load new locations

    locations = driver.find_elements_by_class_name("stores__store")
    for location in locations:

        # Scroll to location
        action = ActionChains(driver)
        action.move_to_element(location).perform()

        # Scrape
        data = location.find_element_by_class_name(
            "store__address").text.split("\n")
        address = data[0] + ", " + data[1]
        phone = location.find_element_by_class_name(
            "store__phone").text[1:].replace(") ", "-").replace(" ", "")
        remote_id = location.get_attribute("id")

        # Objectify
        store_object = {"address": address, "phone": phone, "id": remote_id}
        chain["stores"].append(store_object)
        print(f"{len(chain['stores'])} | Added {store_object}")

    # Scroll back to dropdown button
    action = ActionChains(driver)
    action.move_to_element(dropdown).perform()

with open("../Outputs/shoprite.json", "w") as file:
    json.dump(chain, file, indent=2)
driver.close()
