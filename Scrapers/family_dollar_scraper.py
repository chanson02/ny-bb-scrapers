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


chain = {"name": "Family Dollar", "stores": []}

driver = webdriver.Chrome('../chromedriver.exe')
driver.get("https://www.familydollar.com/locations/")


def list_items():
    return driver.find_elements_by_class_name("ga_w2gi_lp")


def scrape(container):
    data = container.text.split("\n")
    remote_id = re.sub("[^0-9]", "", data[0])
    address = data[1] + ", " + data[2]
    if len(data) == 5:
        phone = data[3][7:]
    else:
        address += ", " + data[4]
        phone = data[3][7:]
    if len(phone) < 12:
        phone = None

    return {"address": address, "phone": phone, "id": remote_id}


for state_index in range(len(list_items())):
    state = list_items()[state_index]
    state.click()

    for city_index in range(len(list_items()[1:])):
        try:
            city = list_items()[1:][city_index]
        except IndexError:
            continue
        city.click()

        containers = driver.find_elements_by_class_name("forcitypage")
        for container in containers:
            store = scrape(container)
            chain["stores"].append(store)
            print("Added", store)

        driver.back()

    driver.back()


with open("../Outputs/family_dollar.json", "w") as f:
    json.dump(chain, f, indent=2)
print("Done")
