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
driver.get("https://www.ediblearrangements.com/stores/store-locator.aspx")
chain = {"name": "Edible Arrangements", "stores": []}
default_delay = 1

with open("../states.json", "r") as f:
    states = json.load(f)


def move(element):
    ActionChains(driver).move_to_element(element).perform()


search_box = driver.find_element_by_id("txtSearchStore")

for state in states:
    time.sleep(default_delay)

    move(search_box)
    search_box.send_keys(Keys.BACKSPACE * 50)
    search_box.send_keys(state["name"])
    search_box.send_keys(Keys.RETURN)
    time.sleep(default_delay * 2)

    locations = driver.find_elements_by_class_name("aStore")
    for location in locations:
        time.sleep(default_delay)
        try:
            move(location)
        except Exception as e:
            print(f"{state} failed: {e}")
            break

        remote_id = re.sub(
            "[^0-9]", "", location.find_element_by_class_name("StoreListName").text)
        phone = location.find_element_by_class_name("StoreListPhone").text
        address = location.find_element_by_class_name(
            "StoreListAddress").text.replace("\n", ", ")

        store = {"address": address, "phone": phone, "id": remote_id}
        chain["stores"].append(store)
        print("Added", store)

with open("../Outputs/edible_arrangements.json", "w") as f:
    json.dump(chain, f, indent=2)
print("Done")
