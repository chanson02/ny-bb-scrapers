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

default_delay = 2


# chain = {"name": "Save A Lot", "stores": []}
with open("../Outputs/save_alot.json", "r") as f:
    chain = json.load(f)
driver = webdriver.Chrome(executable_path='../chromedriver.exe')
driver.get("https://savealot.com/grocery-stores-near-me")
time.sleep(default_delay)

with open("../states.json") as f:
    states = json.load(f)[30:]

iframe = driver.find_element_by_id("sb-site-embed-iframe")
driver.switch_to.frame(iframe)

search_bar = driver.find_element_by_id("id_location")
for state in states:
    search_bar.send_keys(Keys.BACKSPACE * 50)
    search_bar.send_keys(state["name"])
    search_bar.send_keys(Keys.RETURN)
    time.sleep(default_delay)

    locations = driver.find_elements_by_class_name("sb-location")
    for location in locations:
        ActionChains(driver).move_to_element(location).click().perform()
        address = location.find_elements_by_tag_name(
            "p")[1].text.replace("\n", ", ")
        phone = location.find_element_by_class_name(
            "phone-directions").find_element_by_tag_name("p").text[1:].replace(") ", "-")

        url = location.find_element_by_class_name(
            "sb-location-link-view-location").find_element_by_tag_name("a").get_attribute("href")
        remote_id = url.split("-")[-1]

        store = {"address": address, "phone": phone, "id": remote_id}
        if store not in chain["stores"]:
            chain["stores"].append(store)
            print("Added", store)


with open("../Outputs/save_alot.json", "w") as f:
    json.dump(chain, f, indent=2)
print("Done")
