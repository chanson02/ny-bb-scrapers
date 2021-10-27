def execute():
    url = 'https://locations.schnucks.com/'
    scraper = BaseScraper("Schnucks", url)

    # Select frame
    frame_id = 'lcly-embedded-iframe-inner-0'
    frame = scraper.driver.find_element_by_id(frame_id)
    scraper.frame(frame)

    locations = scraper.driver.find_elements_by_class_name('dl-store-list-tile')
    location_urls = [l.find_element_by_tag_name('a').get_attribute('href') for l in locations]
    for url in location_urls:
        scraper.reload_page(url)
        data = scraper.driver.find_element_by_class_name('landing-header-detail-section').text.split('\n')
        scrape(scraper, data)

    scraper.driver.close()
    return scraper

def scrape(scraper, data):
    address = ', '.join(data[:-1])
    phone = data[-1]
    remote_id = scraper.strip_char(scraper.driver.current_url)

    scraper.add_store(address, phone, remote_id, True)
    return

if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
else:
    from scrapers.base_scraper import BaseScraper
