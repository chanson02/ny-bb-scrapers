

def execute():
    url = 'https://www.dollartree.com/locations/'
    scraper = BaseScraper('Dollar Tree', url)

    for state_url in get_urls(scraper, '//*[@id="sli_container"]/div[2]/table'):
        scraper.driver.get(state_url)
        for city_url in get_urls(scraper, '//*[@id="body_wrap"]/div[2]/table'):
            scraper.driver.get(city_url)
            for location_url in [l.find_element_by_tag_name('a').get_attribute('href') for l in scraper.driver.find_elements_by_class_name('storeinfo_div')]:
                scraper.driver.get(location_url)
                scrape(scraper)


    scraper.driver.close()
    return scraper

def get_urls(scraper, path):
    table = scraper.driver.find_element_by_xpath(path)
    states = get_list(table)
    return [s.get_attribute('href') for s in states]

def get_list(e):
    return e.find_elements_by_class_name('ga_w2gi_lp')

def scrape(scraper):
    data = scraper.driver.find_element_by_xpath("//div[@itemprop='address']").text.split('\n')
    address = ', '.join(data[1:-1])
    phone = data[-1]
    remote_id = data[0]

    scraper.add_store(address, phone, remote_id)
    return

if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
else:
    from scrapers.base_scraper import BaseScraper
