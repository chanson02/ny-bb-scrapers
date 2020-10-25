import time
import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium.common import exceptions

driver = webdriver.Chrome('D:\\Programs\\webdrivers\\chromedriver.exe')
driver.get("https://www.target.com/store-locator/find-stores")

zip_button = driver.find_element_by_xpath(
    "/html/body/div[1]/div[2]/div[2]/div[1]/button")
zip_button.click()
zip_entry = driver.find_element_by_xpath(
    "/html/body/div[1]/div[2]/div[3]/div/form/div[1]/div[1]/div/div/input")
locations_path = "/html/body/div[1]/div[2]/div[4]"


def get_store_info(xpath):
    address = driver.find_element_by_xpath(xpath + "/span/a[1]").text
    phone = driver.find_element_by_xpath(xpath + "/span/a[2]").text
    store = driver.find_element_by_xpath(
        xpath + "/div/a").get_attribute('href').split('/')[-1]
    return {"address": address, "phone": phone, "id": store}


def remove_duplicates(array):
    new_array = []
    for element in array:
        if element not in new_array:
            new_array.append(element)
    return new_array


with open('./postals.json', 'r') as file:
    postals = json.load(file)["Postal Codes"]

chain = {
    "name": "Target",
    "stores": []
}

for postal in postals:
    pos = postals.index(postal)
    length = len(postals)
    print(f"{pos}/{length} ({round(pos/length * 100, 2)}%): {postal}")
    for digit in range(5):
        zip_entry.send_keys(Keys.BACKSPACE)
    zip_entry.send_keys(postal)
    time.sleep(0.1)
    zip_entry.send_keys(Keys.RETURN)
    time.sleep(0.1)

    index = 0
    while True:
        index += 1
        location_path = locations_path + f"/div[{index}]/div/div"

        try:
            WebDriverWait(driver, 0.1).until(
                EC.presence_of_element_located((By.XPATH, location_path))
            )

            store = get_store_info(location_path)
            chain["stores"].append(store)

        except exceptions.NoSuchElementException:
            # Got an advertisement
            pass
        except exceptions.TimeoutException:
            # Found all stores
            break

driver.quit()
chain["stores"] = remove_duplicates(chain["stores"])
print(f"{len(postals)} postal codes found {len(chain['stores'])} stores")
with open('./output.json', 'w') as file:
    json.dump(chain, file, indent=2)
