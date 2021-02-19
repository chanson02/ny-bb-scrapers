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
driver.get("https://www.publix.com/locations")
chain = {"name": "Publix", "stores": []}
default_delay = 1

time.sleep(default_delay)
with open("../postals.json", "r") as f:
    postals = json.load(f)["Postal Codes"]

location_urls = []
search_bar = driver.find_element_by_id('input_ZIPorCity,Stateorstorenumber29')
for postal in postals:
    search_bar.send_keys(Keys.BACKSPACE * 5)
    search_bar.send_keys(postal)
    search_bar.send_keys(Keys.RETURN)
    time.sleep(default_delay * 2)

    try:
        store_list = driver.find_element_by_class_name('store-list')
    except exceptions.NoSuchElementException:
        # No results here
        continue

    store_names = store_list.find_elements_by_class_name("store-name")
    store_urls = [name.get_attribute("href") for name in store_names]
    for url in store_urls:
        if url not in location_urls:
            location_urls.append(url)
            print("Added", url)

for url in location_urls:
    driver.get(url)
    time.sleep(default_delay)

    address = driver.find_element_by_class_name(
        "store-address").text.replace("\n", ", ")
    phone_number = driver.find_element_by_class_name(
        "contact-information").find_element_by_tag_name("a").text
    phone = f"{phone_number[:3]}-{phone_number[3:6]}-{phone_number[6:]}"
    remote_id = re.sub("[^0-9]", "", url)

    store = {"address": address, "phone": phone, "id": remote_id}
    chain["stores"].append(store)
    print("Added", store)

with open("../Outputs/publix.json", "w") as f:
    json.dump(chain, f, indent=2)
print("Done")
