from selenium.common import exceptions

def execute():
    url = 'https://www.hy-vee.com/stores/store-finder-results.aspx?zip=&state=&city=&olfloral=False&olcatering=False&olgrocery=False&olpre=False&olbakery=False&diet=False&chef=False'
    scraper = BaseScraper('Hy-Vee', url)

    list_id = "ctl00_cph_main_content_spuStoreFinderResults_gvStores"
    next_id = "ctl00_cph_main_content_spuStoreFinderResults_gvStores_ctl10_btnNext"
    while True:
        store_list = scraper.driver.find_element_by_id(list_id)
        for location in store_list.find_elements_by_tag_name('tr'):
            scrape(scraper, location)

        try:
            scraper.driver.find_element_by_id(next_id).click()
            scraper.wait()
        except exceptions.NoSuchElementException:
            # No more, Done
            break

    scraper.driver.close()
    return scraper

def scrape(scraper, location):
    data = [d for d in location.text.split('\n')[1:-1] if d[:8] != 'Pharmacy']
    address = ', '.join(data[:-1])
    phone = data[-1]
    remote_id = location.find_element_by_tag_name('a').get_attribute('storeid')

    scraper.add_store(address, phone, remote_id)
    return

if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
else:
    from scrapers.base_scraper import BaseScraper
