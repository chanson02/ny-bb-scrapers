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
driver.maximize_window()
driver.get("https://www.fairwaymarket.com/sm/planning/rsid/183/")
chain = {"name": "Fairway Market", "stores": []}
default_delay = 0.5

time.sleep(default_delay)
driver.find_element_by_id("StoreHeaderButton").click()
time.sleep(default_delay)
driver.find_element_by_id("storeDetails-changeStore").click()
time.sleep(default_delay)
locations = driver.find_elements_by_class_name("StoreItem-sc-kocgfr")
for location in locations:
    data = location.find_element_by_class_name(
        "StoreAddress-sc-wesvpf").text.split("\n")
    address = ", ".join(data[:2])
    phone = data[2]
    remote_id = re.sub("[^0-9]", "", phone)

    store = {"address": address, "phone": phone, "id": remote_id}
    chain["stores"].append(store)
    print("Added", store)

with open("../Outputs/fairway_market.json", "w") as f:
    json.dump(chain, f, indent=2)
print("Done")
