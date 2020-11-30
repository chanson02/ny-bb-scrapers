import json
import time
import pdb

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium.common import exceptions

store = "giantfood"
name = "Giant Food"

driver = webdriver.Chrome('../chromedriver.exe')
driver.get(f"https://stores.{store}.com/")
chain = {
    "name": name,
    "stores": []
}


def scrape_addresses(store_count):
    # Get all addresses from page
    if store_count == 1:
        addresses = [driver.find_elements_by_class_name("c-address")[0]]
        phones = [driver.find_elements_by_class_name(
            "c-phone-number-span")[0]]
    else:
        addresses = driver.find_elements_by_class_name("c-address")
        phones = driver.find_elements_by_class_name("c-phone-number-span")

    for index in range(len(phones)):
        address = addresses[index].text.replace("\n", ", ")
        phone = phones[index].text.replace(") ", "-")[1:]
        remote_id = phone.replace("-", "")

        store_object = {
            "address": address,
            "phone": phone,
            "id": remote_id
        }
        if store_object not in chain["stores"]:
            chain["stores"].append(store_object)
            print("Added", store_object)


state_count = len(driver.find_elements_by_class_name("DirectoryList-itemLink"))
# Go through each state
for state_index in range(state_count):
    states = driver.find_elements_by_class_name("DirectoryList-itemLink")
    state = states[state_index]
    state.click()
    time.sleep(0.1)

    city_count = len(driver.find_elements_by_class_name(
        "DirectoryList-itemLink"))
    if city_count == 0:
        scrape_addresses(0)
    else:
        for city_index in range(city_count):
            cities = driver.find_elements_by_class_name(
                "DirectoryList-itemLink")
            store_counts = driver.find_elements_by_class_name(
                "DirectoryList-itemCount")

            city = cities[city_index]
            store_count = int(store_counts[city_index].text[1:-1])
            city.click()
            time.sleep(0.1)

            scrape_addresses(store_count)
            driver.back()
            time.sleep(0.1)

    driver.back()
    time.sleep(0.1)

driver.quit()
# Write to file
with open(f"../Outputs/{store}.json", "w") as file:
    json.dump(chain, file, indent=2)
