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
driver.get("https://www.raleys.com/store-locator/?search=all")
chain = {"name": "Raley's Supermarkets", "stores": []}
default_delay = 1

locations = driver.find_elements_by_class_name("flex-wrap")
for location in locations:
    address = location.find_element_by_tag_name("address").text
    phone_number = location.find_element_by_class_name(
        "contact-list").find_element_by_tag_name("a").text
    remote_id = re.sub("[^0-9]", "", phone_number)
    phone = f"{remote_id[:3]}-{remote_id[3:6]}-{remote_id[6:]}"

    store = {"address": address, "phone": phone, "id": remote_id}
    chain["stores"].append(store)
    print("Added", store)

with open("../Outputs/raleys.json", "w") as f:
    json.dump(chain, f, indent=2)
print("Done")
