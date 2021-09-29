

def execute():
    url = 'http://www.gristedessupermarkets.com/store-locator/'
    scraper = BaseScraper('Gristedes', url, 5)

    scraper.wait()
    locations = scraper.driver.find_elements_by_class_name('results_entry')
    for location in locations:
        scrape(scraper, location)

    scraper.driver.close()
    return scraper

def scrape(scraper, location):
    remote_id = scraper.strip_char(location.find_element_by_class_name('location_name').text)
    phone = location.find_element_by_class_name('slp_result_phone').text

    class_names = ['slp_result_street', 'slp_result_street2', 'slp_result_citystatezip', 'slp_result_country']
    address_parts = [location.find_element_by_class_name(c).text.strip() for c in class_names]
    address = ', '.join([p for p in address_parts if p != ''])

    scraper.add_store(address, phone, remote_id)
    return

if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
else:
    from scrapers.base_scraper import BaseScraper
