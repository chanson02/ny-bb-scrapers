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
driver.get("https://grocery.gianteagle.com/pd/stores/")
chain = {"name": "Giant eagle", "stores": []}
default_delay = 1.5


def scrape():
    remote_id = driver.current_url.split("/")[-1]
    address = driver.find_element_by_xpath(
        "//div[@itemprop='address']").text.replace("\n", ", ")
    phone = driver.find_element_by_xpath(
        "//span[@itemprop='telephone']").text[4:].replace(") ", "-")

    store = {"address": address, "phone": phone, "id": remote_id}
    chain["stores"].append(store)
    print("Added", store)


state_wrapper = driver.find_element_by_class_name("storeListWrap")
state_buttons = state_wrapper.find_elements_by_tag_name("p")
state_urls = [button.find_element_by_tag_name(
    "a").get_attribute("href") for button in state_buttons]

location_urls = []
for url in state_urls:
    # Scrape if it's just one
    # Else add to queue
    driver.get(url)

    try:
        scrape()
        continue
    except Exception:
        # Multiple locations here
        pass

    locations = driver.find_elements_by_id("storeName")
    location_urls += [l.find_element_by_tag_name(
        "a").get_attribute("href") for l in locations]

for url in location_urls:
    driver.get(url)
    scrape()

with open("../Outputs/giant_eagle.json", "w") as f:
    json.dump(chain, f, indent=2)
print("Done")
