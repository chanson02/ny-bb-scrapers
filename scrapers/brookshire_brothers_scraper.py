from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions

def execute():
    url = 'https://www.brookshirebrothers.com/store-locator'
    scraper = BaseScraper('Brookshire Brothers', url)

    for postal in scraper.postals:
        search(scraper, postal)
        wait(scraper)
        locations = scraper.driver.find_elements_by_class_name('brookshire-brothers')
        for location in locations:
            scrape(scraper, location)

    scraper.driver.close()
    return scraper

def search(scraper, postal):
    search_box = scraper.driver.find_element_by_id('search')
    search_box.send_keys(Keys.BACKSPACE * 5)
    search_box.send_keys(postal)
    search_box.send_keys(Keys.RETURN)
    return

# Wait for website to load
def wait(scraper):
    counter = 0
    while True:
        counter += 1
        if counter > 100:
            return
        result = scraper.driver.find_element_by_id('store-locator-results')
        try:
            result.find_element_by_tag_name('p')
            return
        except exceptions.NoSuchElementException:
            pass

        try:
            result.find_element_by_class_name('stores')
            return
        except exceptions.NoSuchElementException:
            pass

    return


def scrape(scraper, location):
    address = location.find_element_by_class_name('address').text
    phone = location.find_element_by_class_name('phone').text
    remote_id = scraper.strip_char(location.find_element_by_class_name('location').get_attribute('innerHTML'))

    scraper.add_store(address, phone, remote_id)
    return


if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
else:
    from scrapers.base_scraper import BaseScraper
