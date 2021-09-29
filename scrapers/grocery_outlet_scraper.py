from selenium.webdriver.support.ui import Select
from selenium.common import exceptions

def execute():
    url = 'https://groceryoutlet.com/store-locator'
    scraper = BaseScraper('Grocery Outlet', url, 0.5)

    region_ndx = 0
    while True:
        region_ndx += 1
        region_selector = Select(scraper.driver.find_elements_by_name("store_region")[1])
        region_button = scraper.driver.find_elements_by_class_name("btn-search-region")[1]
        scraper.move(region_button)

        try:
            region_selector.select_by_index(region_ndx)
        except exceptions.NoSuchElementException:
            break

        region_button.click()
        scraper.wait(1.5)
        locations = scraper.driver.find_elements_by_class_name('border-bottom')
        for location in locations:
            scrape(scraper, location)
        scraper.scroll(scraper.driver.find_element_by_xpath('/html'), 0.1)

    scraper.driver.close()
    return scraper

def scrape(scraper, location):
    scraper.move(location)
    location.find_element_by_class_name("gtm-expand-store").click()
    data = location.text.split('\n')
    scraper.wait()

    address = data[1] + ', ' + data[2]
    phone = location.find_element_by_class_name('store-phone').text
    remote_id = location.get_attribute('data-store-number')

    scraper.add_store(address, phone, remote_id)
    return


if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
else:
    from scrapers.base_scraper import BaseScraper
