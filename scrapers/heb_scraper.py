from selenium.common import exceptions

def execute():
    url = 'https://www.heb.com/store-locations'
    scraper = BaseScraper('H-E-B', url)

    while True:
        container = scraper.driver.find_element_by_class_name('storelocator-store-list')
        locations = container.find_elements_by_tag_name('li')
        locations = [l for l in locations if l.text != '']
        for location in locations:
            scrape(scraper, location)

        try:
            # Go to next page
            scraper.driver.find_element_by_link_text('Next').click()
        except exceptions.NoSuchElementException:
            # No more pages, Done
            break
    scraper.driver.close()
    return scraper

def scrape(scraper, location):
    address = location.find_element_by_xpath(".//p[@itemprop='address']").text
    phone = location.find_element_by_xpath(".//a[@itemprop='telephone']").text
    remote_id = location.find_element_by_tag_name("button").get_attribute("value")

    scraper.add_store(address, phone, remote_id, True)
    return

if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
else:
    from scrapers.base_scraper import BaseScraper
