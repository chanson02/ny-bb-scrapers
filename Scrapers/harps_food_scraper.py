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
driver.get("https://www.harpsfood.com/StoreLocator/")
chain = {"name": "Harps Food Stores", "stores": []}
default_delay = 0.5

time.sleep(default_delay)
state_container = driver.find_element_by_class_name("col-md-9")
state_labels = state_container.find_elements_by_tag_name("li")
state_anchors = [label.find_element_by_tag_name("a") for label in state_labels]
state_urls = [a.get_attribute("href") for a in state_anchors]

location_urls = []

for state_url in state_urls:
    driver.get(state_url)
    time.sleep(default_delay)

    location_table = driver.find_element_by_class_name("table")
    rows = location_table.find_elements_by_tag_name("tr")[1:]
    for row in rows:
        url = row.find_elements_by_tag_name(
            "td")[-1].find_element_by_tag_name("a").get_attribute("href")
        location_urls.append(url)

for location_url in location_urls:
    driver.get(location_url)
    time.sleep(default_delay)

    container = driver.find_elements_by_class_name("container-fluid")[1]
    store_name = container.find_element_by_tag_name("h3").text
    remote_id = re.sub("[^0-9]", "", store_name)
    address = ", ".join(container.find_element_by_class_name(
        "Address").text.split("\n")[1:])
    phone = driver.find_element_by_class_name(
        "PhoneNumber").text[8:].replace(") ", "-")

    store = {"address": address, "phone": phone, "id": remote_id}
    chain["stores"].append(store)
    print("Added", store)

with open("../Outputs/harps_food.json", "w") as f:
    json.dump(chain, f, indent=2)
print("Done")
