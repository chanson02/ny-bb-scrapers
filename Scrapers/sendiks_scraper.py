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
driver.get("https://www.sendiks.com/my-store/locations")
chain = {"name": "Sendik's Food Market", "stores": []}
default_delay = 0.5
time.sleep(default_delay * 5)

locations = driver.find_elements_by_class_name("fp-panel-item")
for location in locations:
    address = location.find_element_by_class_name(
        "fp-store-address").text.replace("\n", ", ")
    remote_id = re.sub(
        "[^0-9]", "", location.find_element_by_class_name("fp-store-phone").text)
    phone = f"{remote_id[:3]}-{remote_id[3:6]}-{remote_id[6:]}"

    store = {"address": address, "phone": phone, "id": remote_id}
    chain["stores"].append(store)
    print("Added", store)

with open("../Outputs/sendiks.json", "w") as f:
    json.dump(chain, f, indent=2)
print("Done")
