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
driver.get("https://www.newseasonsmarket.com/store-map/")
chain = {"name": "New Seasons Market", "stores": []}
default_delay = 0.5
driver.refresh()

for location in driver.find_elements_by_class_name("show-store-on-map"):
    location.click()
    time.sleep(default_delay)

    address = driver.find_element_by_class_name("address").text
    phone = driver.find_element_by_class_name(
        "phone").text[1:].replace(") ", "-")
    remote_id = re.sub("[^0-9]", "", phone)

    store = {"address": address, "phone": phone, "id": remote_id}
    chain["stores"].append(store)
    print("Added", store)

with open("../Outputs/new_seasons_market.json", "w") as f:
    json.dump(chain, f, indent=2)
print("Done")
