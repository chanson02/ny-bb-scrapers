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
from selenium.webdriver.support.ui import Select

from selenium.common import exceptions

chain = {"name": "Wegmans", "stores": []}

driver = webdriver.Chrome('../chromedriver.exe')
driver.get("https://www.wegmans.com/stores/")
time.sleep(1)
# Close popup
driver.find_element_by_id("cookie_action_close_header").click()


def scrape():
    address = driver.find_element_by_id(
        "storeAddress-desktop").text.replace("\n", ",")
    phone = driver.find_element_by_id("phoneNumHere").text
    remote_id = phone.replace("-", "")

    store_object = {"address": address, "phone": phone, "id": remote_id}
    chain["stores"].append(store_object)
    print("Added", store_object)


main_tab = driver.window_handles[0]
locations = driver.find_elements(By.XPATH, "//*[contains(@id, 'Storelink')]")
for location in locations:
    # Close popup
    try:
        driver.find_element_by_class_name("CloseChat").click()
    except exceptions.ElementNotInteractableException:
        pass

    # Open location in new tab
    try:
        ActionChains(driver).move_to_element(location).key_down(
            Keys.CONTROL).click(location).key_up(Keys.CONTROL).perform()
    except exceptions.JavascriptException:
        # Blank location
        continue
    # Switch to new tab
    driver.switch_to.window(driver.window_handles[-1])

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "storeAddress-desktop")))

    scrape()
    # Switch to main page
    driver.switch_to.window(main_tab)

with open("../Outputs/wegmans.json", "w") as file:
    json.dump(chain, file, indent=2)
driver.close()
