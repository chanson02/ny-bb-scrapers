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


chain = {"name": "Price Chopper", "stores": []}

driver = webdriver.Chrome('../chromedriver.exe')
driver.get("https://stores.pricechopper.com/site-map/US")

body_path = "/html/body/div[2]/div/div/div[3]/div/div/div/div/div[1]/div/div[3]/div[1]"

checked = []
done = False
while not done:
    locations = driver.find_elements_by_class_name("sitemap-location")
    locations = [
        location for location in locations if location.text not in checked]

    # Will stop loop if none found
    done = True
    for location in locations:
        done = False
        checked.append(location.text)

        # Open location in a new tab
        open_new_tab = ActionChains(driver)
        open_new_tab.move_to_element(location)
        open_new_tab.key_down(Keys.CONTROL).click(
            location).key_up(Keys.CONTROL)
        open_new_tab.perform()

        # Switch to new tab
        driver.switch_to.window(driver.window_handles[-1])

        # Scrape location
        address_path = body_path + "/div[1]/div[1]"
        address = driver.find_element_by_xpath(
            address_path).text.replace("\n", ", ")
        phone = driver.find_element_by_class_name(
            "tel-number").text[1:].replace(") ", "-")
        remote_id = re.sub(
            "[^0-9]", "", driver.find_element_by_xpath(body_path + "/h1").text)

        # Make/update store object
        store_object = {"address": address, "phone": phone, "id": remote_id}
        chain["stores"].append(store_object)
        print("Added", store_object)

        # Go back to first tab
        driver.switch_to.window(driver.window_handles[0])

with open("../Outputs/pricechopper.json", "w") as file:
    json.dump(chain, file, indent=2)
driver.close()
