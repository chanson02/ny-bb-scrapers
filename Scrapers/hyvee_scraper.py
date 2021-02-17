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
# USE THIS URL NEXT https://www.hy-vee.com/stores/store-finder-results.aspx
chain = {"name": "Hy-Vee", "stores": []}

list_path = "/html/body/section/form/div[3]/div[1]/div/div/div/div[3]/div/div[1]/div[2]/table/tbody"
final_page_path = "/html/body/section/form/div[3]/div[1]/div/div/div/div[3]/div/div[1]/div[2]/table/tbody/tr[8]/td/table/tbody/tr/td/div/a[5]"
next_button_id = "ctl00_cph_main_content_spuStoreFinderResults_gvStores_ctl10_btnNext"

page_count = int(driver.find_element_by_xpath(final_page_path).text)
for page_index in range(page_count):

    location_index = 0
    try:
        while True:
            location_index += 1
            location_path = list_path + f"/tr[{location_index}]/td[3]/p"
            location = driver.find_element_by_xpath(location_path)

            data = location.text.split("\n")
            numbers = sum(char.isdigit() for char in data[1])
            if numbers < 3:
                offset = 1
            else:
                offset = 0

            address = data[1 + offset] + ', ' + data[2 + offset]
            remote_id = re.sub("[^0-9]", "", data[3 + offset])
            phone = remote_id[:3] + "-" + remote_id[3:6] + '-' + remote_id[6:]

            store_object = {"address": address,
                            "phone": phone, "id": remote_id}
            chain["stores"].append(store_object)
            print("Added", store_object)
    except exceptions.NoSuchElementException:
        # No more stores
        # Go to next page
        driver.find_element_by_id(next_button_id).click()
        time.sleep(1)

with open("../Outputs/hyvee.json", "w") as file:
    json.dump(chain, file, indent=2)
