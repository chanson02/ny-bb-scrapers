import json
import time
import pdb
import re

from selenium import webdriver

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium.common import exceptions


chain = {"name": "Giant Eagle", "stores": []}

driver = webdriver.Chrome('../chromedriver.exe')
driver.get("https://www.gianteagle.com/store-locator")
time.sleep(1)

completed = []
done = False

while not done:
    locations = driver.find_elements_by_class_name("store-name-v2")
    locations = [
        location for location in locations if location.text not in completed]

    # Will be done if for loop not activated
    done = True
    for location in locations:
        done = False
        completed.append(location.text)

        open_new_tab = ActionChains(driver)
        open_new_tab.move_to_element(location)
        open_new_tab.key_down(Keys.CONTROL).click(
            location).key_up(Keys.CONTROL)
        open_new_tab.perform()
        time.sleep(1)

        # Switch to that tab
        driver.switch_to.window(driver.window_handles[-1])

        if driver.current_url == "https://www.getgocafe.com/error.html?aspxerrorpath=/stores":
            # Error webpage
            print("Error")
            # Back to original page
            driver.switch_to.window(driver.window_handles[0])
            continue

        addresses = driver.find_elements_by_class_name("store-address")
        address = addresses[6].text + ", " + addresses[7].text

        phone = driver.find_elements_by_class_name(
            "icon-container")[1].text[1:].replace(") ", "-")

        remote_id = re.sub("[^0-9]", "", driver.current_url)

        store_object = {"address": address, "phone": phone, "id": remote_id}
        chain["stores"].append(store_object)

        # Go back to first tab
        driver.switch_to.window(driver.window_handles[0])

with open("../Outputs/gianteagle.json", "w") as file:
    json.dump(chain, file, indent=2)
driver.close()
