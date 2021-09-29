

def execute():
    url = 'https://www.dierbergs.com/mydierbergs/locations'
    scraper = BaseScraper('Dierbergs', url)

    locations = scraper.driver.find_elements_by_class_name('location-listing-item-store')
    for location in locations:
        scrape(scraper, location)

    scraper.driver.close()
    return scraper

def scrape(scraper, location):
    class_names = ["address", "city", "state", "zip"]
    address = ', '.join([location.find_element_by_class_name(c).text.strip() for c in class_names])
    phone = location.find_element_by_class_name('phone').text

    scraper.add_store(address, phone)
    return

if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
else:
    from scrapers.base_scraper import BaseScraper
