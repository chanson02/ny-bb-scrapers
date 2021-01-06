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


chain = {"name": "Grocery Outlet", "stores": []}

driver = webdriver.Chrome('../chromedriver.exe')
driver.get("https://groceryoutlet.com/store-locator")

region_selector = Select(driver.find_elements_by_name("store_region")[1])
region_button = driver.find_elements_by_class_name("btn-search-region")[1]

region_index = 0
while True:
    region_index += 1
    try:
        region_selector.select_by_index(region_index)
    except exceptions.NoSuchElementException:
        break

    region_button.click()
    time.sleep(2)

    locations = driver.find_elements_by_class_name("border-bottom")
    for location in locations:
        ActionChains(driver).move_to_element(location).perform()

        remote_id = location.get_attribute("data-store-number")
        data = location.text.split("\n")
        address = data[1] + ", " + data[2]
        location.find_element_by_class_name("gtm-expand-store").click()
        time.sleep(0.2)
        raw_phone = location.find_element_by_class_name("store-phone").text
        phone = raw_phone[:3] + "-" + raw_phone[3:6] + "-" + raw_phone[6:]

        store = {"address": address, "phone": phone, "id": remote_id}
        if store not in chain["stores"]:
            chain["stores"].append(store)
            print("Added", store)

    # Scroll back to the top
    region_selector = Select(driver.find_elements_by_name("store_region")[1])
    region_button = driver.find_elements_by_class_name("btn-search-region")[1]
    ActionChains(driver).move_to_element(region_button).perform()


with open("../Outputs/grocery_outlet.json", "w") as file:
    json.dump(chain, file, indent=2)
print("Done")
