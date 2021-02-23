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
driver.get("https://centralmarket.com/locations/")
chain = {"name": "Central Market", "stores": []}
default_delay = 0.5

rows = driver.find_elements_by_class_name("elementor-row")
# If no store hours, location is closing
locations = [l for l in rows if "\nSTORE HOURS\n" in l.text]

for location in locations:
    data = location.find_element_by_class_name(
        "elementor-text-editor").text.split("\n")
    address = ", ".join(data[:2])
    phone = data[2]
    remote_id = re.sub("[^0-9]", "", phone)

    store = {"address": address, "phone": phone, "id": remote_id}
    chain["stores"].append(store)
    print("Added", store)

with open("../Outputs/central_market.json", "w") as f:
    json.dump(chain, f, indent=2)
print("Done")
