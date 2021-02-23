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
driver.get("https://www.dagnyc.com/my-store/store-locator")
chain = {"name": "D'agostino", "stores": []}
time.sleep(5)

location_table = driver.find_element_by_class_name("fp-panel-list")
locations = location_table.find_elements_by_tag_name("li")
for location in locations:
    remote_id = location.get_attribute("data-store-number")
    address = location.find_element_by_class_name(
        "fp-store-address").text.replace("\n", ", ")
    phone = location.find_element_by_class_name(
        "fp-store-phone").find_element_by_tag_name("p").text[15:].replace(") ", "-")

    store = {"address": address, "phone": phone, "id": remote_id}
    chain["stores"].append(store)
    print("Added", store)

with open("../Outputs/dagostino.json", "w") as f:
    json.dump(chain, f, indent=2)
print("Done")
