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
driver.get("https://www.superonefoods.com/store-finder")
chain = {"name": "Super One Foods", "stores": []}
default_delay = 0.5
time.sleep(default_delay)
table = driver.find_element_by_class_name("table")
rows = table.find_elements_by_tag_name("tr")[1:]
for row in rows:
    column = row.find_elements_by_tag_name("td")[0]
    data = column.text.split("\n")
    address = ", ".join(data[1:3])
    remote_id = re.sub("[^0-9]", "", data[3])
    phone = f"{remote_id[:3]}-{remote_id[3:6]}-{remote_id[6:]}"

    store = {"address": address, "phone": phone, "id": remote_id}
    chain["stores"].append(store)
    print("Added", store)

with open("../Outputs/super_one_foods.json", "w") as f:
    json.dump(chain, f, indent=2)
print("Done")
print(len(chain["stores"]))
