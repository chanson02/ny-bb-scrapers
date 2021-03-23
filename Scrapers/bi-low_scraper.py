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
driver.get("https://www.bi-lo.com/locator")
chain = {"name": "BI-LO", "stores": []}

with open("../postals.json", "r") as f:
    postals = json.load(f)["Postal Codes"]


search_bar = driver.find_element_by_id("txtStoreQuery")
for postal in postals:
    search_bar.send_keys(Keys.BACKSPACE * 5)
    search_bar.send_keys(postal)
    search_bar.send_keys(Keys.RETURN)
    search_bar = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "txtStoreQuery")))

    tables = driver.find_elements_by_id("strGrdView")
    if len(tables) == 0:
        # No locations
        continue

    locations = tables[0].find_elements_by_class_name("tableStoreHolder")
    for location in locations:
        location_items = location.find_elements_by_tag_name("li")

        remote_id = re.sub(
            "[^0-9]", "", location_items[1].find_element_by_tag_name("a").text)
        address = ", ".join(
            [l.text for l in location_items[1].find_elements_by_tag_name("div")[1:3]])

        phone_numbers = re.sub(
            "[^0-9]", "", location_items[2].find_element_by_tag_name("div").text)
        phone = f'{phone_numbers[:3]}-{phone_numbers[3:6]}-{phone_numbers[6:]}'

        store = {"address": address, "phone": phone, "id": remote_id}
        if store not in chain["stores"]:
            chain["stores"].append(store)
            print("Added", store)

with open("../Outputs/bi-lo.json", "w") as f:
    json.dump(chain, f, indent=2)
print("Done")
