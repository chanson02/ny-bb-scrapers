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
driver.get("https://locations.enmarket.com/")
chain = {"name": "Enmarket", "stores": []}
time.sleep(1)

with open("../postals.json", "r") as f:
    postals = json.load(f)["Postal Codes"]

for postal in postals:
    search_bar = driver.find_element_by_id("location-input")
    search_bar.send_keys(Keys.BACKSPACE * 5)
    search_bar.send_keys(postal)
    search_bar.send_keys(Keys.RETURN)

    results = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "search-center")))
    if results.text[:12] == "0 found near":
        continue

    locations = driver.find_elements_by_class_name("result")
    for location in locations:
        address = ", ".join(
            [e.text for e in location.find_elements_by_class_name("c-AddressRow")])
        phone = location.find_element_by_class_name(
            "phone").text[:1].replace(") ", "-")
        remote_id = re.sub("[^0-9]", "", phone)

        store = {"address": address, "phone": phone, "id": remote_id}
        if store not in chain["stores"]:
            chain["stores"].append(store)
            print("Added", store)

with open("../Outputs/enmarket.json", "w") as f:
    json.dump(chain, f, indent=2)
print("Done")
