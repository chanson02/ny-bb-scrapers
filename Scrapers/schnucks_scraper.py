import json
import time
import pdb
import re

from selenium import webdriver

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium.common import exceptions

driver = webdriver.Chrome('../chromedriver.exe')
driver.get("https://locations.schnucks.com/")
time.sleep(3)

chain = {"name": "Schnucks", "stores": []}
completed = []
done = False

while not done:
    done = True

    locations = driver.find_elements_by_class_name("ListItem-sc-13ek9j9")
    locations = [
        location for location in locations if location.text not in completed]

    # If this for loop is not triggered the program will end
    for location in locations:
        done = False
        completed.append(location.text)

        # Scroll to that element
        actions = ActionChains(driver)
        actions.move_to_element(location).perform()

        address = location.find_element_by_class_name("sls-address").text
        phone = location.find_element_by_xpath(
            "./a/div/span/a[1]").get_attribute("href")[-12:]
        remote_id = re.sub(
            "[^0-9]", "", location.find_element_by_xpath("./a").get_attribute("href"))

        store_object = {"address": address, "phone": phone, "id": remote_id}
        chain["stores"].append(store_object)
        print("Added", store_object)

with open("../Outputs/schnucks.json", "w") as file:
    json.dump(chain, file, indent=2)
print("Done")
driver.close()
