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
driver.get("https://www.marketofchoice.com/locations/")
chain = {"name": "Market of Choice", "stores": []}

panels = driver.find_elements_by_partial_link_text("DISCOVER")
urls = [p.get_attribute("href") for p in panels]
for url in urls:
    driver.get(url)
    address = driver.find_element_by_xpath(
        "/html/body/div[2]/div[2]/main/div/section/div/div/div[1]/div/div[1]/div/div[1]/div/div[5]/div[2]/div/div[1]/p/a").text.replace("\n", ", ")
    try:
        phone = driver.find_element_by_xpath(
            "/html/body/div[2]/div[2]/main/div/section/div/div/div[1]/div/div[1]/div/div[1]/div/div[7]/a/span[2]").text
    except Exception:
        # 'Now Open' gets in the way
        phone = driver.find_element_by_xpath(
            "/html/body/div[2]/div[2]/main/div/section/div/div/div[1]/div/div[1]/div/div[1]/div/div[8]/a/span[2]").text
    remote_id = re.sub("[^0-9]", "", phone)

    store = {"address": address, "phone": phone, "id": remote_id}
    chain["stores"].append(store)
    print("Added", store)

with open("../Outputs/market_choice.json", "w") as f:
    json.dump(chain, f, indent=2)
print("Done")

# /html/body/div[2]/div[2]/main/div/section/div/div/div[1]/div/div[1]/div/div[1]/div/div[7]/a/span[2]
# /html/body/div[2]/div[2]/main/div/section/div/div/div[1]/div/div[1]/div/div[1]/div/div[8]/a/span[2]
