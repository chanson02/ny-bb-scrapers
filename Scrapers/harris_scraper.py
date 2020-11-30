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
driver.get("https://locations.harristeeter.com/")

chain = {"name": "Harris Teeter", "stores": []}

list_path = "/html/body/div[1]/div[2]/div/div/div/div[1]/div/div[2]/div"
state_list_path = list_path + "/div[2]"
city_list_path = list_path + "/div[3]"

# Count how many states there are
state_count = 0
try:
    while True:
        state_count += 1
        state_path = state_list_path + f"/ul[{state_count}]/li/a"
        driver.find_element_by_xpath(state_path)
except exceptions.NoSuchElementException:
    # No more states left
    state_count -= 1

for state_index in range(state_count):

    # Find the state button
    state_path = state_list_path + f"/ul[{state_index + 1}]/li/a"
    state = driver.find_element_by_xpath(state_path)
    state.click()

    # Click on a city
    city_index = 0
    try:
        while True:
            city_index += 1
            city_path = city_list_path + f"/div[{city_index}]/a"
            city = driver.find_element_by_xpath(city_path)
            city.click()

            # Click on location
            location_index = 0
            try:
                while True:
                    location_index += 1
                    location_path = city_list_path + \
                        f"/ul/li[{location_index}]/a"
                    location = driver.find_element_by_xpath(location_path)
                    location.click()

                    # Scrape location data
                    potential_data = driver.find_elements_by_class_name(
                        "find_location_result_left")
                    for data in potential_data:
                        if data.text != '':
                            store_data = data.text.split("\n")
                            break

                    address = store_data[1] + ", " + store_data[2]
                    phone = driver.find_element_by_link_text("CALL STORE").get_attribute(
                        "onclick").split(":")[-1][1:-2].replace(") ", "-")
                    remote_id = driver.current_url.split("/")[-2]
                    store = {
                        "address": address,
                        "phone": phone,
                        "id": remote_id
                    }
                    chain["stores"].append(store)
                    print("Added", store)

                    # Go back to locations
                    driver.back()

            except exceptions.NoSuchElementException:
                # Ran out of locations
                pass

            # Go back to cities
            driver.back()

    except exceptions.NoSuchElementException:
        # Ran out of cities
        pass

    # Go back to states
    driver.back()


# Write to file
with open("../Outputs/harris_teeter.json", "w") as file:
    json.dump(chain, file, indent=2)
