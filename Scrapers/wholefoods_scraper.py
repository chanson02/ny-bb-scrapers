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
driver.get("https://www.wholefoodsmarket.com/stores")

chain = {"name": "Whole Foods", "stores": []}

# Load states
with open("../states.json", "r") as file:
    states = json.load(file)

# Close popup
driver.find_element_by_xpath(
    "/html/body/main/nav/wfm-login-tooltip/div/div/button").click()

search_bar = driver.find_element_by_id("store-finder-search-bar")

for state in states:

    search_bar.send_keys(Keys.BACKSPACE * 50)
    search_bar.send_keys(state["name"])
    search_bar.send_keys(Keys.RETURN)
    time.sleep(1)

    # Uses phones because unopened locations do not have an assigned phone
    phones = driver.find_elements_by_class_name("phone")

    for phone in phones:
        parent = phone.find_element_by_xpath("..")
        address = ", ".join(parent.text.split("\n")[3:5])
        phone_num = phone.text[1:].replace(") ", "-")
        remote_id = phone_num.replace("-", "")

        store_object = {"address": address,
                        "phone": phone_num, "id": remote_id}
        if store_object not in chain["stores"]:
            chain["stores"].append(store_object)
            print("Added", store_object)

with open("../Outputs/wholefoods.json", "w") as file:
    json.dump(chain, file, indent=2)
