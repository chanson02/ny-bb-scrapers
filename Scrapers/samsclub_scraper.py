import json
import time
import pdb
import traceback

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium.common import exceptions

driver = webdriver.Chrome('../chromedriver.exe')
driver.get("https://www.samsclub.com/locator")
time.sleep(1)

last_written_postal = "00501"


def load_postals():
    with open('../postals.json', 'r') as file:
        postals = json.load(file)["Postal Codes"]
    return postals[postals.index(last_written_postal):]


def load_chain():
    with open("../Outputs/samsclub.json", "r") as file:
        chain = json.load(file)
    return chain


def write_output(chain, postal):
    with open("../Outputs/samsclub.json", "w") as file:
        json.dump(chain, file, indent=2)


def main():
    global last_written_postal
    postals = load_postals()
    chain = load_chain()
    driver.get("https://www.samsclub.com/locator")

    for postal in postals:

        # Close popups
        try:
            driver.find_element_by_xpath(
                "/html/body/div[2]/div/div/div[2]/div[1]/button").click()
            driver.find_element_by_xpath(
                "/html/body/div[2]/div/div/div[2]/div[1]/button").click()
            driver.find_element_by_xpath(
                "/html/body/div[2]/div/div/div[2]/div[1]/button").click()
        except exceptions.NoSuchElementException:
            # Closed popups
            pass

        search_box = driver.find_element_by_id("inputbox2")
        search_box.send_keys(Keys.BACKSPACE * 20)
        search_box.send_keys(postal)
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)

        locations = driver.find_elements_by_class_name("sc-club-card-content")
        for location in locations:
            data = location.text.split("\n")

            address = data[3] + ", " + data[4]
            phone = data[5][1:-15].replace(") ", "-")
            remote_id = data[1][4:]

            store_object = {"address": address,
                            "phone": phone, "id": remote_id}
            if store_object not in chain["stores"]:
                chain["stores"].append(store_object)
                write_output(chain, postal)
                last_written_postal = postal
                print(f"{len(chain['stores'])} Stores added | {store_object}")


while True:
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        print(e)
