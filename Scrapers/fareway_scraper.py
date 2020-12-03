import json
import time
import pdb
import re

from selenium import webdriver

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium.common import exceptions


chain = {"name": "Fareway", "stores": []}

driver = webdriver.Chrome('../chromedriver.exe')
driver.get("https://www.fareway.com/stores/ia/adel")

checked_cities = []
done = False

while not done:
    # Open dropdown menu
    dropdown = driver.find_element_by_id("select2-cityState-container")
    dropdown.click()
    time.sleep(0.5)

    cities = driver.find_elements_by_class_name("select2-results__option")
    for city in cities:
        # Check to see if done
        if len(cities) == len(checked_cities):
            done = True

        # Skips over cities already checked
        if city.text in checked_cities:
            continue

        # Scrolls to city and selects it
        actions = ActionChains(driver)
        actions.move_to_element(city).perform()
        checked_cities.append(city.text)
        city.click()
        time.sleep(1)

        # Scrapes store data for city
        addresses = driver.find_elements_by_class_name("card-subtitle")
        phones = driver.find_elements_by_class_name("store-phone")
        ids = driver.find_elements_by_class_name("card-title")

        # Creates object for each location in city
        for index in range(len(addresses)):
            address = addresses[index].text
            try:
                phone = phones[index].text.split(
                    "\n")[1][1:].replace(") ", "-")
            except IndexError:
                phone = "999-999-9999"
                print("Phone not found")
            remote_id = re.sub("[^0-9]", "", ids[index].text)

            store_object = {"address": address,
                            "phone": phone, "id": remote_id}
            chain["stores"].append(store_object)
            print("Added", store_object)

        # Go to the next city
        break

with open("../Outputs/fareway.json", "w") as file:
    json.dump(chain, file, indent=2)
print("Done")
