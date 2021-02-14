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
driver.get("https://www.shoppersfood.com/stores/search-stores.html")
chain = {"name": "Shoppers Food", "stores": []}
default_delay = 0.5
time.sleep(default_delay)


def get_states():
    states_container = driver.find_element_by_id("find-view-states")
    states = states_container.find_elements_by_class_name("cell")
    return states


def scrape_list():
    location_list = driver.find_element_by_xpath(
        "/html/body/ng-app/div[1]/div[3]/div/main/div/div/div/div[2]/div/div/div/div/div[3]/ul")
    locations = location_list.find_elements_by_tag_name("li")
    for location in locations:
        try:
            address = location.find_element_by_class_name(
                "store-address").text + ", " + location.find_element_by_class_name("store-city-state-zip").text
        except:
            continue
        phone_number = re.sub(
            "[^0-9]", "", location.find_element_by_class_name("store-main-phone").text)
        phone = f"{phone_number[:3]}-{phone_number[3:6]}-{phone_number[6:]}"
        remote_id = re.sub("[^0-9]", "", location.find_element_by_class_name(
            "store-detail").get_attribute("alt"))

        store = {"address": address, "phone": phone, "id": remote_id}
        chain["stores"].append(store)
        print("Added", store)


for state_index in range(len(get_states())):
    time.sleep(default_delay)
    state = get_states()[state_index]
    state.find_element_by_tag_name("a").click()
    time.sleep(default_delay)

    nav_bar = driver.find_element_by_class_name("standardPagination")
    try:
        page_count = int(nav_bar.text.split(" ")[-2])
    except ValueError:
        # One page
        page_count = 1
    for page_index in range(page_count):
        scrape_list()
        if page_index != page_count - 1:
            driver.find_element_by_link_text("Next").click()
        time.sleep(default_delay)

    driver.get("https://www.shoppersfood.com/stores/search-stores.html")

with open("../Outputs/shoppers_food.json", "w") as f:
    json.dump(chain, f, indent=2)
print("Done")
