from selenium.common import exceptions

def execute():
    url = 'https://www.foodland.com/store-locations'
    scraper = BaseScraper('Foodland', url)

    while True:
        locations = scraper.driver.find_elements_by_class_name('col-sm-8')
        for location in locations:
            scrape(scraper, location)

        try:
            scraper.driver.find_element_by_link_text('Next Page').click()
        except exceptions.NoSuchElementException:
            break

    scraper.driver.close()
    return scraper

def scrape(scraper, location):
    address = location.find_element_by_class_name('adr').text
    phone = scraper.strip_char(location.find_elements_by_tag_name('a')[1].text)
    scraper.add_store(address, phone)
    return

if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
else:
    from scrapers.base_scraper import BaseScraper
