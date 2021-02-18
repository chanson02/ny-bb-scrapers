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
driver.get("https://www.winndixie.com/locator")
chain = {"name": "Winn-Dixie", "stores": []}
default_delay = 10

time.sleep(default_delay)
container = driver.find_element_by_id("result_accordion")
locations = container.find_elements_by_class_name("p-5")[1:]
for location in locations:
    address = location.find_element_by_class_name(
        "col-lg-12").text.replace("\n", ", ")
    phone = location.find_elements_by_class_name(
        "locator-phone")[1].text[1:].replace(") ", "-")
    remote_id = re.sub(
        "[^0-9]", "", location.find_elements_by_tag_name("div")[2].get_attribute("id"))

    store = {"address": address, "phone": phone, "id": remote_id}
    chain["stores"].append(store)
    print("Added", store)

with open("../Outputs/winn-dixie.json", "w") as f:
    json.dump(chain, f, indent=2)
print("Done")
