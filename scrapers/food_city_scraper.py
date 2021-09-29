

def execute():
    url = 'https://www.foodcity.com/stores/find-a-store'
    scraper = BaseScraper('Food City', url)

    while True:
        locations = scraper.driver.find_elements_by_class_name('store-info')
        for location in locations:
            scrape(scraper, location)

        buttons = scraper.driver.find_elements_by_tag_name('button')
        more_button = [b for b in buttons if b.text == 'See more']
        if len(more_button) == 0:
            break
        else:
            scraper.move(more_button[0])
            more_button[0].click()

    scraper.driver.close()
    return scraper

def scrape(scraper, location):
    remote_id = scraper.strip_char(location.find_element_by_class_name('store-name').text)
    address = location.find_element_by_class_name('address').text
    phone = location.find_element_by_class_name('tel').text

    scraper.add_store(address, phone, remote_id)
    return

if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
else:
    from scrapers.base_scraper import BaseScraper
