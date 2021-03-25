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
driver.get("https://lowesmarket.com/find-store/")
chain = {"name": "Lowe's Market", "stores": []}
default_delay = 2

radius_selector = Select(driver.find_element_by_id("radiusSelect"))
radius_selector.select_by_index(len(radius_selector.options) - 1)

with open("../states.json", "r") as f:
    states = json.load(f)

for state in states:
    search_bar = driver.find_element_by_id("addressInput")
    search_bar.send_keys(Keys.BACKSPACE * 50)
    search_bar.send_keys(state["name"])
    search_bar.send_keys(Keys.RETURN)
    time.sleep(default_delay)

    table = driver.find_element_by_id("map_sidebar")
    if table.text == "No locations found.":
        continue
    locations = table.find_elements_by_class_name("location_primary")

    for location in locations:
        ActionChains(driver).move_to_element(location).click().perform()
        time.sleep(default_delay)

        remote_id = re.sub(
            "[^0-9]", "", driver.find_element_by_id("slp_bubble_name").text)
        address = ", ".join([driver.find_element_by_id("slp_bubble_address").text.replace(",", "").strip(), driver.find_element_by_id(
            "slp_bubble_city").text.replace(",", "").strip(), driver.find_element_by_id("slp_bubble_state").text.replace(",", "").strip(), driver.find_element_by_id("slp_bubble_zip").text.replace(",", "").strip()])
        phone_numbers = re.sub(
            "[^0-9]", "", driver.find_element_by_id("slp_bubble_phone").text)
        phone = f'{phone_numbers[:3]}-{phone_numbers[3:6]}-{phone_numbers[6:]}'

        store = {"address": address, "phone": phone, "id": remote_id}
        if store not in chain["stores"]:
            chain["stores"].append(store)
            print("Added", store)

with open("../Outputs/lowes_market.json", "w") as f:
    json.dump(chain, f, indent=2)
print("Done")
