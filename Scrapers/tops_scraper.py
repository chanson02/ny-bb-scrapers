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


chain = {"name": "Tops", "stores": []}

driver = webdriver.Chrome('../chromedriver.exe')
driver.get("https://www.topsmarkets.com/StoreLocator/")


def scrape():
    address = ", ".join(driver.find_element_by_class_name(
        "Address").text.split("\n")[1:])
    phone = driver.find_element_by_class_name(
        "PhoneNumber").text[8:].replace(") ", "-")
    remote_id = re.sub(
        "[^0-9]", "", driver.find_element_by_class_name("StoreNumber").text)

    store_object = {"address": address, "phone": phone, "id": remote_id}
    chain["stores"].append(store_object)
    print("Added", store_object)


try:
    state_index = 0
    while True:
        container = driver.find_element_by_class_name("col-md-9")
        state_items = container.find_elements_by_tag_name("li")
        state_items[state_index].find_element_by_tag_name("a").click()

        try:
            location_index = 0
            while True:
                location_links = driver.find_elements_by_link_text("View")
                location_element = location_links[location_index]
                # Scroll to location
                ActionChains(driver).move_to_element(
                    location_element).perform()
                location_element.click()

                scrape()
                # Go back to locations view
                driver.back()
                location_index += 1
        except IndexError:
            # Ran out of locations in state
            pass

        # Go back to states view
        driver.back()
        state_index += 1


except IndexError:
    # Out of states
    pass

with open("../Outputs/tops.json", "w") as file:
    json.dump(chain, file, indent=2)
driver.close()
