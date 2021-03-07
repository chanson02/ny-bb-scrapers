import json
import time
import pdb
import re

from selenium import webdriver

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium.common import exceptions

default_delay = 0.5


def get_hrefs():
    content = driver.find_element_by_class_name("content")
    hrefs = [anchor.get_attribute(
        "href") for anchor in content.find_elements_by_tag_name("a")[1:]]
    return hrefs


chain = {"name": "Save a Lot", "stores": []}
driver = webdriver.Chrome(executable_path='../chromedriver.exe')
driver.get("https://savealot.com/grocery-stores/")
time.sleep(default_delay)

city_urls = []
location_urls = []
for state_url in get_hrefs():
    driver.get(state_url)
    time.sleep(default_delay)
    city_urls += get_hrefs()

for city_url in city_urls:
    try:
        driver.get(city_url)
        time.sleep(default_delay)
        location_urls += get_hrefs()[1:]
    except:
        pdb.set_trace()

for location_url in location_urls:
    try:
        driver.get(location_url)
        time.sleep(default_delay)

        address = driver.find_element_by_class_name(
            "address").text.replace("\n", ", ")
        phone = driver.find_element_by_class_name(
            "phone").text[1:].replace(") ", "-")
        remote_id = location_url.split("-")[-1][:-1]

        store = {"address": address, "phone": phone, "id": remote_id}
        chain["stores"].append(store)
        print("Added", store)
    except:
        pdb.set_trace()

with open("../Outputs/save_alot.json", "w") as f:
    json.dump(chain, f, indent=2)
print("Done")
