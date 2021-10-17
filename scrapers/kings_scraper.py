

def execute():
    url = 'https://kingsfoodmarkets.com/locations'
    scraper = BaseScraper('Kings', url)
    scraper.wait()

    locations = scraper.driver.find_elements_by_class_name('views-row')
    for location in locations:
        scrape(scraper, location)

    scraper.driver.close()
    return scraper

def scrape(scraper, location):
    address = location.find_element_by_class_name('views-field-field-store-address').text
    phone = location.find_element_by_class_name('views-field-field-phone').text
    scraper.add_store(address, phone, debug=True)
    return

if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
else:
    from scrapers.base_scraper import BaseScraper
