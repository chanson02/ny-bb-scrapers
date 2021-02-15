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
driver.get("https://www.rosauers.com/store-locations/")
chain = {"name": "Rosauers Supermarkets", "stores": []}
default_delay = 0.5

locations = driver.find_elements_by_class_name("location")
for location in locations:
    data = location.text.split("\n")
    address = data[1][9:]
    remote_id = re.sub("[^0-9]", "", data[3])
    phone = f"{remote_id[:3]}-{remote_id[3:6]}-{remote_id[6:]}"

    store = {"address": address, "phone": phone, "id": remote_id}
    chain["stores"].append(store)
    print("Added", store)

with open("../Outputs/rosauers.json", "w") as f:
    json.dump(chain, f, indent=2)
print("Done")
