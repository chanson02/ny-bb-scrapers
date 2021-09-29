

def execute():
    url = 'https://www.earthfare.com/stores/'
    scraper = BaseScraper('Earth Fare', url, 3)

    locations = scraper.driver.find_elements_by_class_name('elementor-text-editor')
    for location in locations:
        scrape(scraper, location)

    scraper.driver.close()
    return scraper

def scrape(scraper, location):
    data = location.text.split('\n')
    address = ', '.join(data[1:3])
    try:
        phone = data[3]
    except IndexError:
        # Upcoming Address
        return

    scraper.add_store(address, phone)
    return

if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
else:
    from scrapers.base_scraper import BaseScraper
