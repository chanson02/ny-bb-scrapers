import json
import time
import pdb

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium.common import exceptions

driver = webdriver.Chrome('D:\\Programs\\webdrivers\\chromedriver.exe')
driver.get("https://www.rulerfoods.com/locations")

chain = {"name": "Ruler Foods", "stores": []}


def write_output():
    with open("../Outputs/rulerfoods.json", "w") as file:
        json.dump(chain, file, indent=2)


# Remove popup
driver.find_element_by_class_name("popup-close").click()
location_path = f"/html/body/div[2]/div[1]/div[1]/div/div[3]/div[2]/div[1]/div[1]/div/div[2]"
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, location_path)))

# Scroll page
driver.execute_script("window.scrollTo(0, 1000);")

page_selected = 1
while True:

    for location_index in range(1, 6):
        location_path = f"/html/body/div[2]/div[1]/div[1]/div/div[3]/div[2]/div[1]/div[{location_index + 5 * (page_selected - 1)}]/div/div[2]"
        try:
            WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.XPATH, location_path)))
        except exceptions.TimeoutException:
            # No more locations
            write_output()
            exit()

        location = driver.find_element_by_xpath(location_path)
        data = location.text.split("\n")
        address = data[0]
        phone = ''.join(data[1].split(" ")[-2:])[1:].replace(")", "-")
        remote_id = phone.replace("-", "")

        store_object = {"address": address, "phone": phone, "id": remote_id}
        chain["stores"].append(store_object)
        print("Added", store_object)

    # Go to next page
    page_selected += 1
    time.sleep(1)
    pages = driver.find_elements_by_class_name("numbers")
    # pdb.set_trace()
    for page in pages:
        if page.text == str(page_selected):
            page.click()
            break
