

def execute():
    url = 'https://www.jerrysfoods.com/my-store/store-locator'
    scraper = BaseScraper("Jerry's Foods", url)

    locations = scraper.driver.find_elements_by_class_name('fp-store-info')
    for location in locations:
        scrape(scraper, location)

    scraper.driver.close()
    return scraper

def scrape(scraper, location):
    address = location.find_element_by_class_name('fp-store-address').text
    phone = location.find_element_by_class_name('fp-store-phone').text

    scraper.add_store(address, phone, debug=True)
    return

if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
else:
    from scrapers.base_scraper import BaseScraper
