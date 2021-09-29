def execute():
    url = 'https://www.marketofchoice.com/locations/'
    scraper = BaseScraper("Market of Choice", url)

    panels = scraper.driver.find_elements_by_partial_link_text('DISCOVER')
    urls = [p.get_attribute('href') for p in panels]
    [scrape(scraper, url) for url in urls]

    scraper.driver.close()
    return scraper

def scrape(scraper, url):
    scraper.driver.get(url)
    address = scraper.driver.find_element_by_xpath("/html/body/div[2]/div[2]/main/div/section/div/div/div[1]/div/div[1]/div/div[1]/div/div[5]/div[2]/div/div[1]/p/a").text.replace("\n", ", ")
    try:
        phone = scraper.driver.find_element_by_xpath(
            "/html/body/div[2]/div[2]/main/div/section/div/div/div[1]/div/div[1]/div/div[1]/div/div[7]/a/span[2]").text
    except Exception:
        # 'Now Open' gets in the way
        phone = scraper.driver.find_element_by_xpath(
            "/html/body/div[2]/div[2]/main/div/section/div/div/div[1]/div/div[1]/div/div[1]/div/div[8]/a/span[2]").text

    scraper.add_store(address, phone)
    return

if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
else:
    from scrapers.base_scraper import BaseScraper
