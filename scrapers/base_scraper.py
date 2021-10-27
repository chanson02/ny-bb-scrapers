import re
import time
import json

from selenium import webdriver

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By

# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support.ui import Select

# from selenium.common import exceptions

class BaseScraper:
    def __init__(self, name, url, dd=1, eager=False):
        self.name = name.replace("'", "''")
        self.url = url
        self.stores = []

        self.postals = self.load_postals()
        self.states = self.load_states()

        self.set_caps(eager)
        self.reload_window()
        self.default_delay = dd
        self.wait()

    def __repr__(self):
        return self.name

    # Function to load all US postal codes from JSON
    def load_postals(self):
        with open('postals.json', 'r') as f:
            postals = json.load(f)['Postal Codes']
        return postals

    # Function to load all US states from JSON
    def load_states(self):
        with open('states.json', 'r') as f:
            states = json.load(f)
        return states

    def set_caps(self, eager):
        self.caps = DesiredCapabilities().CHROME
        if eager:
            self.caps['pageLoadStrategy'] = 'eager'
        return

    # Function to create a new window
    def reload_window(self):
        try:
            self.driver.close()
        except Exception:
            # driver is already closed
            pass

        self.driver = webdriver.Chrome('./chromedriver', desired_capabilities=self.caps)
        self.driver.delete_all_cookies()
        self.reload_page()
        return

    # Function to refresh the tab
    def reload_page(self, url=None):
        if url is None:
            url = self.url
        self.driver.get(url)
        return

    def wait(self, extra=0):
        time.sleep(self.default_delay + extra)

    # Function to remove letters from a string
    def strip_char(self, string):
        if string is None:
            return ''
        return re.sub('[^0-9]', '', string)

    # Function to add store to stores payload
    def add_store(self, address, phone, remote_id=None, debug=False):
        address = address.replace("'", "''").replace('\n', ', ')
        phone = self.strip_char(phone)
        if len(phone) < 10:
            phone = None
            if remote_id is None:
                print(f' ! {self.name} - |{address}| has no phone or id')
                return
        else:
            if remote_id is None:
                remote_id = phone
            phone = f'{phone[:3]}-{phone[3:6]}-{phone[6:]}'

        if not remote_id.isnumeric():
            # print(f'{self.name} Scraper returned non-numeric ID: {remote_id} ! Stripping non-ints')
            remote_id = self.make_numeric(remote_id)

        store = {'address': address.replace("'", "''"), 'phone': phone, 'id': remote_id}
        if store not in self.stores:
            self.stores.append(store)
            if debug:
                if remote_id is None:
                    remote_id = ''
                if phone is None:
                    phone = ''
                template = 'Added store to {0:10} - | {1:4} | {2:12} | {3}'
                print(template.format(self.name, remote_id, phone, address))
        return

    # Function to scroll page to find element
    def move(self, elem):
        ActionChains(self.driver).move_to_element(elem).perform()
        return

    # Function to scroll down all the way on an element
    # Loads more and keeps scrolling
    def scroll(self, elem, timeout=3):
        updated = time.time()
        old_height = 0
        height = self.driver.execute_script('return arguments[0].scrollHeight;', elem)
        while time.time() - updated < timeout:
            height = self.driver.execute_script('return arguments[0].scrollHeight;', elem)
            if height != old_height:
                updated = time.time()
                self.driver.execute_script('arguments[0].scrollTo(0,arguments[1]);', elem, height)
                old_height = height
        return

    # Function to remove non-int values from string
    def make_numeric(self, str):
        result = ''
        for c in str:
            if c.isdigit():
                result += c
        return result

    # Function to select different 'iframe's
    def frame(self, frame):
        self.driver.switch_to.frame(frame)
        return



"""
def execute():
    url = ''
    scraper = BaseScraper("", url)

    scraper.driver.close()
    return scraper

def scrape(scraper, location):
    scraper.add_store(address, phone, remote_id)
    return

if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
    print(f'found {len(scraper.stores)} stores')
else:
    from scrapers.base_scraper import BaseScraper
"""
