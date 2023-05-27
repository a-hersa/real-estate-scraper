
import os
import sys
from src.logger import logging
from src.exception import CustomException

import requests
from bs4 import BeautifulSoup
import time

url_key = 1
class Scrapingant():
    def __init__(self, url):
        logging.info('Initializing Scrapingant class')
        self.url = url

    def url_to_soup(self):
        global url_key
        logging.info('Initializing url_to_soup function')
        encoded_url = requests.utils.quote(self.url, safe='')
        req_url = f'https://api.scrapingant.com/v2/general?url={encoded_url}&x-api-key={os.getenv(f"SCRAPINGANT_KEY{url_key}")}&browser=false'
        print(f'https://api.scrapingant.com/v2/general?url={encoded_url}&x-api-key={os.getenv(f"SCRAPINGANT_KEY{url_key}")}&browser=false')
        r = requests.get(req_url)
        logging.info(f'key is {os.getenv(f"SCRAPINGANT_KEY{url_key}")}')
        logging.info(f'status code is {r.status_code}') # 403 response code means you run out of API calls
        if r.status_code == 403:
            url_key += 1
        soup = BeautifulSoup(r.text, 'lxml')        
        show = soup.prettify().split('\n')
        logging.info(f'second line is {show[1]}')
        while show[1] != '<html class="" data-userauth="false" env="es" lang="es" username="">':
            logging.info(f'second line is {show[1]}')
            logging.info('second line of soup was found different than what it should be')
            time.sleep(10)
            req_url = f'https://api.scrapingant.com/v2/general?url={encoded_url}&x-api-key={os.getenv(f"SCRAPINGANT_KEY{url_key}")}&browser=false'
            r = requests.get(req_url)
            logging.info(f'key is {os.getenv(f"SCRAPINGANT_KEY{url_key}")}')
            logging.info(f'status code is {r.status_code}')
            if r.status_code == 403:
                url_key += 1
            soup = BeautifulSoup(r.text, 'lxml')
            show = soup.prettify().split('\n')
        logging.info(f'{str(show[:5])}')
        return soup