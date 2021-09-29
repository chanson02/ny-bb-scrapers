

def execute():
    url = 'https://www.fairwaymarket.com/sm/planning/rsid/183/'
    scraper = BaseScraper('Fairway Market', url)

    scraper.driver.maximize_window()
    scraper.driver.find_element_by_id("StoreHeaderButton").click()
    scraper.wait()
    scraper.driver.find_element_by_id("storeDetails-changeStore").click()
    scraper.wait()
    content = scraper.driver.find_element_by_class_name('Content-sc-1y8v2ch')
    scraper.scroll(content)

    locations = scraper.driver.find_elements_by_class_name("StoreItem-sc-kocgfr")
    for location in locations:
        scrape(scraper, location)

    scraper.driver.close()
    return scraper

def scrape(scraper, location):
    data = location.find_element_by_class_name('StoreAddress-sc-wesvpf').text.split('\n')
    address = ', '.join(data[:2])
    phone = data[2]

    scraper.add_store(address, phone)
    return

if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
else:
    from scrapers.base_scraper import BaseScraper
