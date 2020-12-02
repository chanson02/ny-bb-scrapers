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
driver.get("https://www.foodlion.com/stores/")

with open('../postals.json', 'r') as file:
    postals = json.load(file)["Postal Codes"]

with open('../Outputs/foodlion.json', 'r') as file:
    chain = json.load(file)

# Wait for page to load
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "sidebar-content")))

for postal in postals:

    # Type in search box
    search = driver.find_element_by_id("flStoreSearch")
    search.send_keys(Keys.BACK_SPACE * 5)
    search.send_keys(postal)
    search.send_keys(Keys.RETURN)
    time.sleep(0.1)

    # Get info from sidebar
    sidebar = driver.find_element_by_id("sidebar-content")
    content = sidebar.text

    # If nothing was found continue
    if content == "No matching search results, please try again.":
        continue
    else:
        stores_info = content.split(
            "\nHours/Details >\nDirections >\nWEEKLY SPECIALS\n")

        for store_info in stores_info:
            info = store_info.split("\n")
            address = info[2] + ", " + info[3]
            phone = info[4]
            remote_id = phone.replace("-", "")

            store_object = {"address": address,
                            "phone": phone, "id": remote_id}
            if store_object not in chain["stores"]:
                chain["stores"].append(store_object)
                print("Added", store_object)
                print("Store Count:", len(chain["stores"]))

with open("../Outputs/foodlion.json", "w") as file:
    json.dump(chain, file, indent=2)
