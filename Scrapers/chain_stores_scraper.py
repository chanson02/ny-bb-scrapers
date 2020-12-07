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

#!-- Works with
# Weis Markgets
# Brookshires

name = "Brookshire's"
base_url = "brookshires"

chain = {"name": "Weis", "stores": []}
driver = webdriver.Chrome('../chromedriver.exe')
driver.get(f"https://www.{base_url}.com/stores")
time.sleep(3)


popup_id = "guessed-store-popover-dismiss-button"
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, popup_id)))
    driver.find_element_by_id(popup_id).click()
except exceptions.TimeoutException:
    pass

locations = driver.find_elements_by_class_name("store-list__rail")
for location in locations:

    # Click on location
    ActionChains(driver).move_to_element(location).perform()
    location.click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "store-details-pane__scroll-container")))
    time.sleep(1)

    # Looking at location data
    container = driver.find_element_by_class_name(
        "store-details-pane__scroll-container")
    data = location.find_element_by_class_name(
        "store-preview__info").text.split("\n")

    # Parse location data
    address = data[4] + ", " + data[5]
    phone_numbers = re.sub("[^0-9]", "", container.find_element_by_class_name(
        "store-details-store-contact__list-item-entry--value").text)
    phone = phone_numbers[:3] + "-" + \
        phone_numbers[3:6] + "-" + phone_numbers[6:]
    remote_id = re.sub("[^0-9]", "", data[2])

    # Create object and store it
    store_object = {"address": address, "phone": phone, "id": remote_id}
    chain["stores"].append(store_object)
    print("Added", store_object)

    # Go back to view all
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.CLASS_NAME, "store-details-pane__back-button")))
    time.sleep(1)
    driver.find_element_by_class_name(
        "store-details-pane__back-button").click()

with open(f"../Outputs/{base_url}.json", "w") as file:
    json.dump(chain, file, indent=2)
driver.close()
