

def execute():
    url = 'https://centralmarket.com/locations/'
    scraper = BaseScraper('Central Market', url)

    rows = scraper.driver.find_elements_by_class_name('elementor-row')
    # If no store hours, location is closing
    locations = [l for l in rows if "\nSTORE HOURS\n" in l.text]
    for location in locations:
        scrape(scraper, location)

    scraper.driver.close()
    return scraper

def scrape(scraper, location):
    data = location.find_element_by_class_name('elementor-text-editor').text.split('\n')
    address = ', '.join(data[:2])
    phone = data[2]
    scraper.add_store(address, phone)

if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
else:
    from scrapers.base_scraper import BaseScraper
