from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def execute():
    url = 'https://locations.enmarket.com/'
    scraper = BaseScraper('Enmarket', url)

    for postal in scraper.postals:
        search(scraper, postal)

        results = WebDriverWait(scraper.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'search-center')))
        if results.text[:12] == '0 found near':
            continue

        locations = scraper.driver.find_elements_by_class_name('results')
        for location in locations:
            scrape(scraper, location)

    scraper.driver.close()
    return scraper

def search(scraper, postal):
    search_bar = scraper.driver.find_element_by_id('location-input')
    search_bar.send_keys(Keys.BACKSPACE * 100)
    search_bar.send_keys(postal)
    search_bar.send_keys(Keys.RETURN)

def scrape(scraper, location):
    address = ', '.join([e.text for e in location.find_elements_by_class_name('c-AddressRow')])
    phone = location.find_element_by_class_name('phone').text
    scraper.add_store(address, phone)
    return

if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
else:
    from scrapers.base_scraper import BaseScraper
