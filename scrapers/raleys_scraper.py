def execute():
    url = 'https://www.raleys.com/store-locator/?search=all'
    scraper = BaseScraper("Raley's Supermarkets", url)

    locations = scraper.driver.find_elements_by_class_name('flex-wrap')
    [scrape(scraper, l) for l in locations]

    scraper.driver.close()
    return scraper

def scrape(scraper, location):
    address = location.find_element_by_tag_name('address').text
    phone = location.find_element_by_class_name("contact-list").find_element_by_tag_name("a").text
    scraper.add_store(address, phone)
    return

if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
else:
    from scrapers.base_scraper import BaseScraper
