

def execute():
    url = 'https://www.gelsons.com/stores'
    scraper = BaseScraper('Gelsons Markets', url)

    table = scraper.driver.find_element_by_tag_name('ol')
    locations = table.find_elements_by_tag_name('li')
    for location in locations:
        scrape(scraper, location)

    scraper.driver.close()
    return scraper

def scrape(scraper, location):
    data = location.find_elements_by_tag_name('a')
    address = data[0].text
    phone = data[1].text

    scraper.add_store(address, phone)
    return

if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
else:
    from scrapers.base_scraper import BaseScraper
