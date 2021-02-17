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
driver.get("https://www.priceritemarketplace.com/store")
chain = {"name": "Price Rite", "stores": []}
default_delay = 0.5

locations = driver.find_elements_by_class_name("StoreItem-sc-kocgfr")
for location in locations:
    if location.text == "":
        # Empty location
        continue

    data = location.find_element_by_class_name(
        "StoreAddress-sc-wesvpf").text.split("\n")
    address = ", ".join(data[:2])

    try:
        remote_id = data[2]
        phone = f"{remote_id[:3]}-{remote_id[3:6]}-{remote_id[6:]}"
    except IndexError:
        remote_id = None
        phone = None

    store = {"address": address, "phone": phone, "id": remote_id}
    chain["stores"].append(store)
    print("Added", store)

with open("../Outputs/price_rite.json", "w") as f:
    json.dump(chain, f, indent=2)
print("Done")
