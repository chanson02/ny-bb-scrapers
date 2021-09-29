

def execute():
    url = 'https://www.familydollar.com/locations/'
    scraper = BaseScraper('Familly Dollar', url)

    state_urls = [s.get_attribute('href') for s in get_list(scraper.driver)]
    for state in state_urls:
        scraper.driver.get(state)
        city_urls = [c.get_attribute('href') for c in get_list(scraper.driver)]

        for city in city_urls:
            scraper.driver.get(city)

            locations = scraper.driver.find_elements_by_class_name('forcitypage')
            for location in locations:
                scrape(scraper, location)

    scraper.driver.close()
    return scraper

def get_list(e):
    return e.find_elements_by_class_name('ga_w2gi_lp')

def scrape(scraper, location):
    data = location.text.split('\n')
    remote_id = scraper.strip_char(data[0])
    address = data[1] + ', ' + data[2]

    if len(data) == 5:
        phone = data[3][7:]
    else:
        address += ', ' + data[3]
        phone = data[4][7:]

    if len(phone) < 12:
        phone = None

    scraper.add_store(address, phone, remote_id)
    return

if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
else:
    from scrapers.base_scraper import BaseScraper
