import json
import time
import pdb
import re
import traceback

from selenium import webdriver

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

from selenium.common import exceptions

driver = webdriver.Chrome('../chromedriver.exe')
driver.get("https://www.brookshirebrothers.com/store-locator")
last_written_postal = "00501"

with open("../postals.json", "r") as file:
    all_postals = json.load(file)["Postal Codes"]


def load_chain():
    with open("../Outputs/brookshirebrothers.json", "r") as file:
        chain = json.load(file)
    return chain


def write_output(chain):
    with open("../Outputs/brookshirebrothers.json", "w") as file:
        json.dump(chain, file, indent=2)


def scrape(location):
    address = location.find_element_by_class_name(
        "address").text.replace("\n", ", ")
    phone = location.find_element_by_class_name(
        "phone").text[1:].replace(") ", "-")
    remote_id = re.sub(
        "[^0-9]", "", location.find_element_by_class_name("location").get_attribute("innerHTML"))

    store = {"address": address, "phone": phone, "id": remote_id}
    return store


def main():
    global driver
    global last_written_postal

    chain = load_chain()
    postals = all_postals[all_postals.index(last_written_postal):]

    search_box = driver.find_element_by_id("search")
    for postal in postals:

        # Look up postal
        search_box.send_keys(Keys.BACKSPACE * 5)
        search_box.send_keys(postal)
        search_box.send_keys(Keys.RETURN)
        time.sleep(1)

        locations = driver.find_elements_by_class_name("brookshire-brothers")
        # Put a wait here?
        for location in locations:
            ActionChains(driver).move_to_element(location)

            store_object = scrape(location)
            if store_object not in chain["stores"]:
                chain["stores"].append(store_object)
                print("Added", store_object)
                write_output(chain)
            last_written_postal = postal

    # All postals done
    write_output(chain)
    exit()
    print("Done")


while True:
    try:
        main()
    except KeyboardInterrupt:
        pdb.set_trace()
        exit()
    except Exception as e:
        print(e)
        traceback.print_exc()
        driver = webdriver.Chrome('../chromedriver.exe')
        driver.get("https://www.brookshirebrothers.com/store-locator")
