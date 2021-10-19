from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions
import time
import traceback

def execute():
    url = 'https://www.publix.com/locations'
    scraper = BaseScraper('Publix', url, dd=0.5)
    urls = []

    ndx = scraper.postals.index('32004')
    for postal in scraper.postals[ndx: ndx+10]:
        attempt = 0
        while attempt < 10:
            try:
                attempt += 1
                search(scraper, postal)
                wait_page_load(scraper, postal)
                try:
                    store_list = scraper.driver.find_element_by_class_name('store-list')
                except exceptions.NoSuchElementException:
                    # No results
                    break # Break while loop
                store_names = store_list.find_elements_by_class_name('store-name')
                store_urls = [name.get_attribute('href') for name in store_names]
                [urls.append(u) for u in store_urls if u not in urls]
                break #Break while loop
            except exceptions.WebDriverException:
                # WebDriver crashed
                scraper.reload_window()
                # print('\n\nEXPECTED EXCEPTION')
                # traceback.print_exc()
                # print('\n')
                scraper.wait(10)
                if attempt > 5:
                    import pdb; pdb.set_trace()
            except KeyboardInterrupt:
                import pdb; pdb.set_trace()

    [scrape(scraper, url) for url in urls]

    scraper.driver.close()
    return scraper

def search(scraper, postal):
    # bar = scraper.driver.find_element_by_id('input_ZIPorCity,Stateorstorenumber29') #the 29 at the end changed to 46?
    bar = scraper.driver.find_elements_by_tag_name('input')[2]
    bar.send_keys(Keys.BACKSPACE * 5)
    bar.send_keys(postal)
    bar.send_keys(Keys.RETURN)
    return

# Wait for map update
def wait_page_load(scraper, postal):
    start = time.time()
    while time.time() - start < 1.5:
        result = scraper.driver.find_element_by_class_name('results-column')
        try:
            if postal in result.text:
                return
        except IndexError:
            pass
            # this was returning?
    return

def scrape(scraper, url):
    scraper.driver.get(url)

    try:
        address = scraper.driver.find_element_by_class_name('store-address').text
        phone = scraper.driver.find_element_by_class_name('contact-information').find_element_by_tag_name('a').text
        # remote_id = scraper.strip_char(url)
        remote_id = url.split('/')[-1].split('-')[0]

        scraper.add_store(address, phone, remote_id, True)
    except exceptions.NoSuchElementException:
        return
    return


if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
else:
    from scrapers.base_scraper import BaseScraper
