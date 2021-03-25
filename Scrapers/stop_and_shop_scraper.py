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
driver.get("https://stores.stopandshop.com/")
chain = {"name": "Stop & Shop", "stores": []}
default_delay = 0.5
time.sleep(default_delay)


def scrape():

    try:
        address = ", ".join(
            [e.text for e in driver.find_elements_by_class_name("c-AddressRow")[:2]])
        phone = driver.find_element_by_id(
            "telephone").text[1:].replace(") ", "-")
        remote_id = re.sub(
            "[^0-9]", "", driver.find_element_by_class_name("StoreDetails-storeNum").text).lstrip("0")

        store = {"address": address, "phone": phone, "id": remote_id}
        chain["stores"].append(store)
    except exceptions.NoSuchElementException:
        # Store Permanently closed error
        return


lst = driver.find_element_by_class_name("DirectoryList-content")
items = lst.find_elements_by_class_name("DirectoryList-itemLink")
state_urls = [e.get_attribute("href") for e in items]
for state_url in state_urls:
    driver.get(state_url)
    time.sleep(default_delay)
    lst = driver.find_element_by_class_name("DirectoryList-content")
    items = lst.find_elements_by_class_name("DirectoryList-itemLink")
    city_urls = [e.get_attribute("href") for e in items]

    for city_url in city_urls:
        driver.get(city_url)
        time.sleep(default_delay)

        lst = driver.find_elements_by_class_name("LocationList")
        if len(lst) == 0:
            scrape()
        else:
            location_urls = [e.get_attribute(
                "href") for e in driver.find_elements_by_link_text("View Page")]

            for location_url in location_urls:
                driver.get(location_url)
                time.sleep(default_delay)
                scrape()


with open("../Outputs/stopandshop.json", "w") as f:
    json.dump(chain, f, indent=2)

print("Done")
