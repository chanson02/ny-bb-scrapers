import re, traceback
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions

def execute():
    url = 'https://www.caseys.com/store-finder/locations'
    scraper = BaseScraper("Casey's", url)
    scraper.wait()


    store_urls = []
    for postal in scraper.postals:
        for _ in range(5): # Attempt this try/except 5 times
            try:
                search(scraper, postal)
                store_urls += [u for u in scrape_urls(scraper) if u not in store_urls]
                break #break the try/except

            except exceptions.WebDriverException:
                scraper.reload_window()
                scraper.wait()

    for url in store_urls:
        try:
            scrape(scraper, url)
        except Exception:
            print("Casey's Scraper Failed on a URL")
            traceback.print_exc()

    scraper.driver.close()
    return scraper

def search(scraper, postal):
    search_bar = scraper.driver.find_element_by_class_name('pac-target-input')
    search_bar.send_keys(Keys.BACKSPACE * 100)
    # search_bar.send_keys(f'{postal}, USA')
    search_bar.send_keys(postal)
    search_bar.send_keys(Keys.RETURN)
    scraper.wait()
    return

def scrape_urls(scraper):
    urls = []
    store_cards = scraper.driver.find_elements_by_class_name('mb-3')
    for card in store_cards:
        try:
            url = card.find_element_by_tag_name('a').get_attribute('href').split('?')[0]
            urls.append(url)
        except exceptions.NoSuchElementException:
            break
    return urls

def scrape(scraper, url):
    scraper.driver.get(url)
    scraper.wait()
    elements = scraper.driver.find_elements_by_class_name('ml-3')

    remote_id = url.split('/')[-1]
    address = re.sub(' +', ' ', elements[0].text[9:-15])
    phone = elements[1].text

    scraper.add_store(address, phone, remote_id)
    return

if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
else:
    from scrapers.base_scraper import BaseScraper
