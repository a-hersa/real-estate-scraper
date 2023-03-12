
import requests
from bs4 import BeautifulSoup
import time
import os
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s', '%Y-%m-%d %H:%M:%S')

file_handler = logging.FileHandler('scraper.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

class Scrapingant():
    def __init__(self, url):
        logger.debug('Initializing Scrapingant class')
        self.url = url

    def url_to_soup(self):
        logger.debug('Initializing url_to_soup function')
        encoded_url = requests.utils.quote(self.url, safe='')
        req_url = f'https://api.scrapingant.com/v2/general?url={encoded_url}&x-api-key={os.getenv("SCRAPINGANT_KEY")}'
        r = requests.get(req_url)
        soup = BeautifulSoup(r.text, 'lxml')
        return soup

    # Same methods for multiple requests
    def urls_to_soups(self):
        logger.debug('Initializing urls_to_soups function')
        all_soups = []
        for url in self.url:
            time.sleep(10)
            try:
                encoded_url = requests.utils.quote(url, safe='')
                req_url = f'https://api.scrapingant.com/v2/general?url={encoded_url}&x-api-key={os.getenv("SCRAPINGANT_KEY")}'
                r = requests.get(req_url)
                soup = BeautifulSoup(r.text, 'lxml')
                all_soups.append(soup)
            except:
                logger.exception(f'Exception with {url} occurred')
        return all_soups