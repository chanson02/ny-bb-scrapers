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
driver.get("https://lundsandbyerlys.com/our-stores/locations/")
chain = {"name": "Lunds & Byerlys", "stores": []}
default_delay = 0.5
time.sleep(3)
container = driver.find_element_by_id("wpsl-stores")
locations = container.find_elements_by_tag_name("li")
for location in locations:
    data = location.find_element_by_class_name(
        "wpsl-addressLeft").text.split("\n")
    address = ", ".join(data[1:3])
    phone = data[3].replace("(", "").replace(") ", "-")
    remote_id = location.get_attribute("data-store-id")

    store = {"address": address, "phone": phone, "id": remote_id}
    chain["stores"].append(store)
    print("Added", store)

with open("../Outputs/lunds_byerlys.json", "w") as f:
    json.dump(chain, f, indent=2)
print("Done")
