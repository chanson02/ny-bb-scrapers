

def execute():
    url = ''
    scraper = BaseScraper('Fresh Market', url)

    scraper.driver.close()
    return scraper

if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
else:
    from scrapers.base_scraper import BaseScraper
