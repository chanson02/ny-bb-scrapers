def execute():
    url = 'https://www.sendiks.com/my-store/locations'
    scraper = BaseScraper("Sendik's Food Market", url)
    # scraper.wait(5)

    locations = scraper.driver.find_elements_by_class_name('fp-panel-item')
    while len(locations) == 0:
        locations = scraper.driver.find_elements_by_class_name('fp-panel-item')
    [scrape(scraper, l) for l in locations]

    scraper.driver.close()
    return scraper

def scrape(scraper, location):
    address = location.find_element_by_class_name('fp-store-address').text
    phone = location.find_element_by_class_name('fp-store-phone').text
    scraper.add_store(address, phone)
    return

if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
else:
    from scrapers.base_scraper import BaseScraper
