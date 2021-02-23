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
driver.get("https://www.lowesfoods.com/store-locator")
chain = {"name": "Lowes Foods", "stores": []}
default_delay = 1

time.sleep(default_delay)
search_bar = driver.find_element_by_tag_name("input")
search_bar.send_keys(Keys.BACKSPACE * 100)
search_bar.send_keys(Keys.RETURN)
time.sleep(default_delay * 3)
urls = [button.get_attribute(
    "href") for button in driver.find_elements_by_link_text("Store Details")]
for url in urls:
    driver.get(url)
    time.sleep(default_delay)
    remote_id = re.sub("[^0-9]", "", url)
    phone = driver.find_element_by_class_name(
        "store-details__store-info__phone").find_element_by_tag_name("a").text
    address_elements = driver.find_element_by_class_name(
        "store-details__store-info").find_elements_by_tag_name("li")[1:4]
    address = ", ".join([e.text for e in address_elements if e.text != ""])

    store = {"address": address, "phone": phone, "id": remote_id}
    chain["stores"].append(store)
    print("Added", store)

with open("../Outputs/lowes_foods.json", "w") as f:
    json.dump(chain, f, indent=2)
print("Done")
