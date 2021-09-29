

def execute():
    url = 'https://www.dagnyc.com/my-store/store-locator'
    scraper = BaseScraper("D'agostino", url)
    scraper.wait(4)

    location_table = scraper.driver.find_element_by_class_name('fp-panel-list')
    locations = location_table.find_elements_by_tag_name('li')
    for location in locations:
        scrape(scraper, location)

    scraper.driver.close()
    return scraper

def scrape(scraper, location):
    remote_id = location.get_attribute('data-store-number')
    address = location.find_element_by_class_name('fp-store-address').text
    phone = location.find_element_by_class_name('fp-store-phone').find_element_by_tag_name('p').text[15:]

    scraper.add_store(address, phone, remote_id)
    return

if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
else:
    from scrapers.base_scraper import BaseScraper
