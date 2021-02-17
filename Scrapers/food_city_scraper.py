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
driver.get("https://www.foodcity.com/stores/find-a-store")
chain = {"name": "Food City", "stores": []}
default_delay = 0.5

while True:
    time.sleep(default_delay)
    locations = driver.find_elements_by_class_name("store-info")
    for location in locations:
        store_name = location.find_element_by_class_name("store-name").text
        remote_id = remote_id = remote_id = re.sub("[^0-9]", "", store_name)
        address = location.find_element_by_class_name(
            "address").text.replace("\n", ", ")
        phone = location.find_element_by_class_name(
            "tel").text.replace(" ", "-")

        store = {"address": address, "phone": phone, "id": remote_id}
        chain["stores"].append(store)
        print("Added", store)

    buttons = driver.find_elements_by_tag_name("button")
    more_button = [b for b in buttons if b.text == "See more"]
    if len(more_button) == 0:
        break

    more_button = more_button[0]
    ActionChains(driver).move_to_element(more_button).perform()
    more_button.click()

with open("../Outputs/food_city.json", "w") as f:
    json.dump(chain, f, indent=2)
print("Done")
