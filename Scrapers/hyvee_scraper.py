import json
import time
import pdb

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium.common import exceptions

import re

driver = webdriver.Chrome('../chromedriver.exe')
driver.get("https://www.hy-vee.com/stores/store-finder-results.aspx?zip=&state=&city=&olfloral=False&olcatering=False&olgrocery=False&olpre=False&olbakery=False&diet=False&chef=False")
chain = {"name": "Hy-Vee", "stores": []}
default_delay = 2

list_id = "ctl00_cph_main_content_spuStoreFinderResults_gvStores"
next_id = "ctl00_cph_main_content_spuStoreFinderResults_gvStores_ctl10_btnNext"
store_list = None

while True:
    time.sleep(default_delay)
    store_list = driver.find_element_by_id(list_id)

    for row in store_list.find_elements_by_tag_name("tr"):
        try:
            data = row.find_elements_by_tag_name("td")[2]
        except:
            continue
        remote_id = data.find_element_by_tag_name("a").get_attribute("storeid")
        lines = [l for l in row.find_element_by_tag_name(
            "p").text.split("\n")[1:-1] if l[:8] != "Pharmacy"]
        phone = lines[-1][6:]
        address = ", ".join(lines[:-1])

        store = {"address": address, "phone": phone, "id": remote_id}
        chain["stores"].append(store)
        print("Added", store)

    try:
        driver.find_element_by_id(next_id).click()
    except Exception:
        # no more pages
        break

with open("../Outputs/hyvee.json", "w") as f:
    json.dump(chain, f, indent=2)
print("Done")
