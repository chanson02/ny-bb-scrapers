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
driver.get("https://www.pigglywiggly.com/store-locations")
chain = {"name": "Piggly Wiggly", "stores": []}
default_delay = 0.5

time.sleep(default_delay)
state_urls = [label.find_element_by_tag_name("a").get_attribute(
    "href") for label in driver.find_elements_by_class_name("field-content")]

for state_url in state_urls:
    driver.get(state_url)
    time.sleep(default_delay)

    location_list = driver.find_element_by_class_name("item-list")
    locations = location_list.find_elements_by_tag_name("li")
    for location in locations:
        address = location.find_element_by_class_name(
            "adr").text.replace("\n", ", ")

        phone_container = location.find_element_by_class_name(
            "views-field-field-phone-value")
        phone = phone_container.find_element_by_class_name(
            "field-content").text.replace("(", "").replace(") ", "-").replace(".", "-")
        remote_id = "".join(phone.split("-"))

        store = {"address": address, "phone": phone, "id": remote_id}
        chain["stores"].append(store)
        print("Added", store)

with open("../Outputs/piggly_wiggly.json", "w") as f:
    json.dump(chain, f, indent=2)
print("Done")
