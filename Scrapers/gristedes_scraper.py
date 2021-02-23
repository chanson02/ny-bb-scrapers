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
driver.get("http://www.gristedessupermarkets.com/store-locator/")
chain = {"name": "Gristedes", "stores": []}
default_delay = 0.5
time.sleep(5)
class_names = ["slp_result_street", "slp_result_street2",
               "slp_result_citystatezip", "slp_result_country"]
locations = driver.find_elements_by_class_name("results_entry")
for location in locations:
    remote_id = re.sub(
        "[^0-9]", "", location.find_element_by_class_name("location_name").text)
    address_parts = [location.find_element_by_class_name(
        c).text.strip() for c in class_names]
    address = ", ".join([p for p in address_parts if p != ""])
    phone = location.find_element_by_class_name("slp_result_phone").text

    store = {"address": address, "phone": phone, "id": remote_id}
    chain["stores"].append(store)
    print("Added", store)

with open("../Outputs/gristedes.json", "w") as f:
    json.dump(chain, f, indent=2)
print("Done")
