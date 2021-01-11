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
driver.get("https://specsonline.com/locations/")
chain = {"name": "Spec's Wine", "stores": []}
default_delay = 0.5


def move(element):
    ActionChains(driver).move_to_element(element).perform()


# Yes, I am 21 or older
driver.find_element_by_id("enter_site_sm_yes").click()

rows = driver.find_elements_by_class_name("viewLocationDetail")
for row_index in range(len(rows)):
    time.sleep(default_delay)

    rows = driver.find_elements_by_class_name("viewLocationDetail")
    row = rows[row_index]
    move(row)
    row.click()  # Open the row

    view_button = driver.find_elements_by_class_name("viewLocationPage")[
        row_index]
    move(view_button)
    view_button.click()
    time.sleep(default_delay)

    try:
        driver.find_element_by_id("enter_site_sm_yes").click()  # 21
    except exceptions.NoSuchElementException:
        pass

    address = driver.find_element_by_xpath(
        "//div[@itemprop='address']").text.replace("\n", ", ")

    try:
        phone = driver.find_element_by_class_name("mobile-off").text
    except exceptions.NoSuchElementException:
        phone = driver.find_element_by_class_name("mobile-off").text

    remote_id = re.sub("[^0-9]", "", phone)

    store = {"address": address, "phone": phone, "id": remote_id}
    chain["stores"].append(store)
    print("Added", store)
    driver.back()

with open("../Outputs/specs_wine.json", "w") as f:
    json.dump(chain, f, indent=2)
print("Done")
