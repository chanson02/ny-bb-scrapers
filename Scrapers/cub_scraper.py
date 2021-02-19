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
driver.get("https://www.cub.com/stores/search-stores.html")
chain = {"name": "Cub", "stores": []}
default_delay = 1

time.sleep(default_delay)
# Viewing states
container = driver.find_element_by_id("find-view-states")
labels = container.find_elements_by_class_name("cell")
state_urls = [l.find_element_by_tag_name(
    "a").get_attribute("href") for l in labels]

for url in state_urls:
    driver.get(url)
    time.sleep(default_delay)

    while True:
        container = driver.find_element_by_id("store-search-results")
        location_list = container.find_element_by_tag_name("ul")
        locations = location_list.find_elements_by_tag_name("li")
        locations = [l for l in locations if len(l.text) > 30]
        for location in locations:
            address = location.find_element_by_class_name(
                "store-address").text + ", " + driver.find_element_by_class_name("store-city-state-zip").text
            phone_number = re.sub(
                "[^0-9]", "", location.find_element_by_class_name("store-main-phone").text)
            phone = f"{phone_number[:3]}-{phone_number[3:6]}-{phone_number[6:]}"
            remote_id = re.sub(
                "[^0-9]", "", location.find_element_by_link_text("See Store Details").get_attribute("href"))

            store = {"address": address, "phone": phone, "id": remote_id}
            chain["stores"].append(store)
            print("Added", store)

        try:
            # Go to next page
            driver.find_element_by_link_text("Next").click()
            time.sleep(default_delay)
        except:
            break

with open("../Outputs/cub.json", "w") as f:
    json.dump(chain, f, indent=2)
print("Done")
