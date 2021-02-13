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
driver.get("https://www.marketofchoice.com/about-market-of-choice/locations")
chain = {"name": "Market of Choice", "stores": []}
default_delay = 0.5

table = driver.find_element_by_xpath("//*[@id='content']/div[2]/div[2]/table")
rows = table.find_elements(By.TAG_NAME, "tr")
for row in rows:
    if rows.index(row) % 2 != 0:
        continue
    ActionChains(driver).move_to_element(row).perform()

    data = row.text.split("\n")
    phone_pos = -2
    if data[-1][0] != "O":
        phone_pos = -1

    phone = data[phone_pos].replace(".", "-")
    address = ", ".join(data[phone_pos-2:phone_pos])
    remote_id = phone.replace("-", "")

    store = {"address": address, "phone": phone, "id": remote_id}
    chain["stores"].append(store)
    print("Added", store)

with open("../Outputs/market_of_choice.json", "w") as f:
    json.dump(chain, f, indent=2)
print("Done")
