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
driver.get("https://www.gelsons.com/stores.html")
chain = {"name": "Gelson's Markets", "stores": []}
default_delay = 0.5
time.sleep(default_delay)
table = driver.find_element_by_id("store-search-results")
locations = table.find_elements_by_tag_name("li")
locations = [l for l in locations if len(l.text) > 30]
for location in locations:
    remote_id = location.get_attribute("data-storeid")
    address = ", ".join([location.find_element_by_class_name(
        "store-address").text, location.find_element_by_class_name("store-city-state-zip").text])
    phone = location.find_element_by_class_name(
        "store-main-phone").text[13:].replace(") ", "-")

    store = {"address": address, "phone": phone, "id": remote_id}
    chain["stores"].append(store)
    print("Added", store)

with open("../Outputs/gelsons_markets.json", "w") as f:
    json.dump(chain, f, indent=2)
print("Done")
