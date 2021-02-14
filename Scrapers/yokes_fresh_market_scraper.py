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
driver.get("https://www.yokesfreshmarkets.com/stores")
chain = {"name": "Yoke's Fresh Market", "stores": []}
default_delay = 0.5

locations = driver.find_elements_by_class_name("views-row")

for location in locations:
    address = location.find_element_by_class_name("address").text
    remote_id = re.sub(
        "[^0-9]", "", location.find_element_by_class_name("store-info").text.split("\n")[-1])
    phone = f"{remote_id[:3]}-{remote_id[3:6]}-{remote_id[6:]}"

    store = {"address": address, "phone": phone, "id": remote_id}
    chain["stores"].append(store)
    print("Added", store)

with open("../Outputs/yokes_fresh_market.json", "w") as f:
    json.dump(chain, f, indent=2)
print("Done")
