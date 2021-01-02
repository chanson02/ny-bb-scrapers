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

chain = {"name": "United Grocery Outlet", "stores": []}

opts = webdriver.ChromeOptions()
opts.add_argument("--ignore-certificate-errors")
opts.add_argument('--ignore-ssl-errors')
driver = webdriver.Chrome(options=opts, executable_path='../chromedriver.exe')
driver.get("https://www.myugo.com/locations/")

addy_xpath = "/html/body/div[2]/div[1]/div[2]/div/article/div/div/div/div[2]/div[2]/div[1]/div/div/div[1]/div/div/div/div/p"

time.sleep(5)
rows = driver.find_elements_by_class_name("et_pb_row")
row_length = len(rows)
for row_index in range(row_length):
    time.sleep(2)

    rows = driver.find_elements_by_class_name("et_pb_row")
    try:
        row = rows[row_index]
    except IndexError:
        break
    try:
        cities = row.find_elements_by_xpath(".//a")
    except exceptions.NoSuchElementException:
        continue

    for city_index in range(len(cities)):
        time.sleep(2)
        rows = driver.find_elements_by_class_name("et_pb_row")
        try:
            row = rows[row_index]
        except IndexError:
            break
        cities = row.find_elements_by_xpath(".//a")
        city = cities[city_index]

        ActionChains(driver).move_to_element(city).perform()
        city.click()
        time.sleep(2)

        try:
            info = driver.find_element_by_xpath(addy_xpath).text.split("\n")
        except exceptions.NoSuchElementException:
            driver.back()
            continue
        address = info[0] + ", " + info[1]
        if len(info) == 3:
            remote_id = re.sub("[^0-9]", "", info[2])
        else:
            remote_id = re.sub("[^0-9]", "", info[3])
            address += ", " + info[2]
        phone = remote_id[:3] + "-" + remote_id[3:6] + "-" + remote_id[6:]
        store = {"address": address, "phone": phone, "id": remote_id}
        chain["stores"].append(store)
        print("Added", store)

        driver.back()


with open(f"../Outputs/united_grocery_outlet.json", "w") as file:
    json.dump(chain, file, indent=2)
driver.close()

print("Done")
