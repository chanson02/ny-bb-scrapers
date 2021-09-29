def execute():
    url = 'https://www.balduccis.com/locations'
    scraper = BaseScraper("Balducci's", url)

    locations = scraper.driver.find_elements_by_class_name('views-row')
    locations = [l for l in locations if l.text != '']
    for l in locations:
        address = l.find_element_by_class_name('views-field-field-store-address').text
        phone = l.find_element_by_class_name('views-field-field-phone').text
        scraper.add_store(address, phone)

    scraper.driver.close()
    return scraper

if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
else:
    from scrapers.base_scraper import BaseScraper
