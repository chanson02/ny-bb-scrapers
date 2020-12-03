import traceback
import sys
import pdb
import time
import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium.common import exceptions

import re

last_written_postal = "23456"


def load_postals():
    # Load in postal data
    with open('../postals.json', 'r') as file:
        postals = json.load(file)["Postal Codes"]
    return postals[postals.index(last_written_postal):]


def load_chain():
    # Load in previously found walmarts
    file = "../Outputs/walmarts.json"
    with open(file, "r") as f:
        chain = json.load(f)
    return chain


def write_output(chain, postal):
    with open("../Outputs/walmarts.json", "w") as file:
        json.dump(chain, file, indent=2)
    global last_written_postal
    last_written_postal = postal


def lookup(driver, postal):
    # Open the search box
    driver.find_element_by_class_name("current-zip").click()
    search_box = driver.find_element_by_class_name("field-input")
    search_box.send_keys(Keys.BACKSPACE * 5)  # Remove old zip
    search_box.send_keys(postal)
    search_box.send_keys(Keys.RETURN)


def scrape_location(driver):
    address = driver.find_element_by_class_name("store-address").text
    phone = driver.find_element_by_id("store-phone").text

    id_html = driver.find_element_by_class_name(
        "store-type-name-and-number").get_attribute("innerHTML")
    id_span = id_html.split("span")[-2]
    remote_id = re.sub("[^0-9]", "", id_span.split("-->")[-2])

    store_object = {
        "address": address,
        "phone": phone,
        "id": remote_id,
    }

    return store_object


def main():
    last_percent = 0
    chain = load_chain()
    postals = load_postals()
    postal_count = len(postals)

    # Open webdriver
    driver = webdriver.Chrome('../chromedriver.exe')
    driver.get("https://walmart.com/store/finder?location=00501&distance=10")

    for postal in postals:
        lookup(driver, postal)
        time.sleep(1)

        location_count = len(
            driver.find_elements_by_class_name("store-details-icon-link"))
        for location_index in range(location_count):
            # The item must be selected for the data to appear
            items = driver.find_elements_by_class_name("store-list-item")
            items[location_index].click()
            time.sleep(1)

            location = driver.find_elements_by_class_name(
                "store-details-icon-link")[location_index]
            location.click()
            time.sleep(1)

            store_object = scrape_location(driver)
            if store_object not in chain["stores"]:
                chain["stores"].append(store_object)
                print("Added", store_object)

            # Go back to locations
            driver.find_element_by_class_name("icon-button-children").click()
            time.sleep(1)

        current_index = postals.index(postal)
        percent = round(current_index / postal_count * 100, 2)
        if percent - last_percent >= 0.5:
            last_percent = percent
            print(f"{percent}%")
            write_output(chain, postal)

    write_output(chain, "99950")
    exit()


# main()
while True:
    try:
        main()
    except KeyboardInterrupt:
        print("Last Postal Write", last_written_postal)
        exit()
    except Exception as e:
        print("Last Postal Write", last_written_postal)
        print(sys.exc_info())
        print(e)
        traceback.print_exc()
        print("RESTARTING")
