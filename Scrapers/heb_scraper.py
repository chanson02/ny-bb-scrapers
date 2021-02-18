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
driver.get("https://www.heb.com/store-locations")
chain = {"name": "H-E-B", "stores": []}
default_delay = 0.5

time.sleep(default_delay)
container = driver.find_element_by_class_name("storelocator-store-list")
while True:
    time.sleep(default_delay)
    # Get this pages locations
    locations = container.find_elements_by_tag_name("li")
    locations = [l for l in locations if l.text != ""]

    # Scrape locations
    for location in locations:
        address = location.find_element_by_xpath(
            ".//p[@itemprop='address']").text.replace("\n", ", ")
        phone = location.find_element_by_xpath(
            ".//a[@itemprop='telephone']").text[1:].replace(")", "-").replace(" ", "")
        remote_id = location.find_element_by_tag_name(
            "button").get_attribute("value")

        store = {"address": address, "phone": phone, "id": remote_id}
        chain["stores"].append(store)
        print("Added", store)

    try:
        # Go to the next page
        driver.find_element_by_link_text("Next").click()
        time.sleep(default_delay)
    except Exception:
        # No more pages
        # Done
        break

with open("../Outputs/heb.json", "w") as f:
    json.dump(chain, f, indent=2)
print("Done")
