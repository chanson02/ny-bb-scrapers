import json
import time
import pdb

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium.common import exceptions

driver = webdriver.Chrome('../chromedriver.exe')
driver.get("https://www.hannaford.com/locations/")

with open("../Outputs/hannaford.json", "r") as file:
    chain = json.load(file)

with open("../postals.json", "r") as file:
    postals = json.load(file)["Postal Codes"]
postals = postals[postals.index("84317"):]
previous_percent = 0

# Remove popups
driver.find_element_by_class_name("tipso_close").click()

for postal in postals:
    percent = round(postals.index(postal) / len(postals) * 100, 0)
    if percent - 5 == previous_percent:
        print(f"{postal} | {percent}%")
        previous_percent = percent
        with open("../Outputs/hannaford.json", "w") as file:
            json.dump(chain, file, indent=2)

    search_box = driver.find_element_by_id("cityStateZip")
    search_box.send_keys(Keys.BACKSPACE * 5)
    search_box.send_keys(postal)
    search_box.send_keys(Keys.RETURN)
    if postal == postals[0]:
        time.sleep(1)

    # Check for popup
    try:
        driver.find_element_by_id("fsrFocusFirst").click()
    except exceptions.NoSuchElementException:
        pass

    # Check if no stores were returned
    try:
        driver.find_element_by_class_name("search-error")
        continue
    except exceptions.NoSuchElementException:
        pass

    stores = driver.find_elements_by_class_name("list-unstyled")
    for store in stores:
        data = store.text.split("\n")
        heading = data[0]
        address = data[3] + ", " + data[4]
        phone = data[5]
        remote_id = driver.find_elements_by_link_text(
            heading)[-1].get_attribute("href")[-5:]

        store_object = {
            "address": address,
            "phone": phone,
            "id": remote_id
        }

        if store_object not in chain["stores"]:
            chain["stores"].append(store_object)
            print("Added", store_object)

with open("../Outputs/hannaford.json", "w") as file:
    json.dump(chain, file, indent=2)
