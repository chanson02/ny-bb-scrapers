import json
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium.common import exceptions

payload = {"name": "Sprouts", "stores": []}

driver = webdriver.Chrome('D:\\Programs\\webdrivers\\chromedriver.exe')
driver.get("https://www.sprouts.com/stores/")

states_path = "/html/body/div[8]/main/article/div/div/div[1]/div[2]/div"
WebDriverWait(driver, 10).until(  # Wait for page to load
    EC.presence_of_element_located((By.XPATH, states_path))
)

state_count = 0

try:
    while True:
        state_count += 1
        state_path = states_path + f'/div[{state_count}]'
        WebDriverWait(driver, 0.1).until(
            EC.presence_of_element_located((By.XPATH, state_path)))
except exceptions.TimeoutException:
    # Close the popup
    popup_path = '/html/body/div[12]/div/div/span'
    x_button = driver.find_element_by_xpath(popup_path)
    x_button.click()

for state_index in range(1, state_count):
    # Wait for states to reappear (After back button clicked)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, states_path))
    )

    print(f"State #{state_index}")
    # Click on the state
    state_path = states_path + f'/div[{state_index}]/a'
    state_button = driver.find_element_by_xpath(state_path)
    state_button.click()

    # Wait for elements to appear
    store_container_path = '/html/body/div[8]/main/div/div'
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, store_container_path))
    )

    # Find how many stores there are
    store_count = 0
    try:
        while True:
            store_count += 1
            store_cell_path = store_container_path + f'/div[{store_count}]'
            WebDriverWait(driver, 0.1).until(
                EC.presence_of_element_located((By.XPATH, store_cell_path))
            )
    except exceptions.TimeoutException:
        pass

    # Loop through stores
    for store_index in range(1, store_count):
        print(f"Store #{store_index}")
        store_cell_path = store_container_path + f'/div[{store_index}]'

        # Remote Id
        id_path = store_cell_path + '/p[1]'
        remote_id = driver.find_element_by_xpath(id_path).text[7:]

        ## Address + Phone
        try:
            other_info_path = store_cell_path + '/p[2]'
            other_info = driver.find_element_by_xpath(
                other_info_path).text.split("\n")
            address = other_info[0] + ', ' + other_info[1]
            # phone = other_info[2]
        except IndexError:
            other_info_path = store_cell_path + '/p[3]'
            other_info = driver.find_element_by_xpath(
                other_info_path).text.split("\n")
            address = other_info[0] + ', ' + other_info[1]

        try:
            phone = other_info[2]
        except IndexError:
            phone = "Null"
            # phone = other_info[2]

        # Update payload
        store = {
            "address": address,
            "phone": phone,
            "id": remote_id
        }
        payload["stores"].append(store)

    # Go back
    driver.back()

with open("sprouts.json", 'w') as f:
    json.dump(payload, f, indent=2)
