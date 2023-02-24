
import requests
from bs4 import BeautifulSoup
import json
import time
import os
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s', '%Y-%m-%d %H:%M:%S')

file_handler = logging.FileHandler('scraper.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

class Scraperapi():
    def __init__(self, url):
        logger.debug('Initializing Scraperapi class')
        self.url = url
    
    def post_request(self):
        logger.debug('Initializing post_request function')
        r = requests.post(url = 'https://async.scraperapi.com/jobs', json={ 'apiKey': os.getenv('SCRAPERAPI_KEY'), 'url': self.url})
        status_url = json.loads(r.text)['statusUrl']
        logger.debug(f'Returning {status_url}')
        logger.debug(status_url)
        return status_url
    
    def get_request(self, status_url):
        logger.debug('Initializing get_request function')
        r = requests.get(url = status_url)
        res = json.loads(r.text)
        status = res['status']
        while status != 'finished':
            logger.debug('Waiting 10 secs...')
            time.sleep(10)
            r = requests.get(url = status_url)
            res = json.loads(r.text)
            status = res['status']
        else:
            res = json.loads(r.text)
        logger.debug('Returning response')
        return res

    def get_soup(self, res):
        logger.debug('Initializing get_soup function')
        soup = BeautifulSoup(res['response']['body'], 'lxml')
        logger.debug('Returning soup')
        return soup

    def url_to_soup(self):
        logger.debug('Initializing url_to_soup function')
        soup = self.get_soup(self.get_request(self.post_request()))
        return soup

    # Same methods for multiple requests
    def post_requests(self):
        logger.debug('Initializing post_requests function')
        r = requests.post(url = 'https://async.scraperapi.com/jobs', json={ 'apiKey': os.getenv('SCRAPERAPI_KEY'), 'urls': self.url})
        status_urls = []
        for i in range(len(self.url)):
            status_urls.append(json.loads(r.text)[i]['statusUrl'])
        logger.debug('Returning list of status_urls')
        for url in status_urls:
            logger.debug(url)
        return status_urls
    
    def get_requests(self, status_urls):
        logger.debug('Initializing get_requests function')
        all_res = []
        for i in range(len(status_urls)):
            logger.debug('Waiting 30 secs...')
            time.sleep(30)
            r = requests.get(url = status_urls[i])
            res = json.loads(r.text)
            status = res['status']
            while status != 'finished':
                logger.debug('Waiting 30 secs...')
                time.sleep(30)
                r = requests.get(url = status_urls[i])
                res = json.loads(r.text)
                status = res['status']
            else:
                all_res.append(json.loads(r.text))
        logger.debug('Returning list with all rersponses')
        return all_res

    def get_soups(self, all_res):
        logger.debug('Initializing get_soups function')
        all_soups = []
        for i in range(len(all_res)):
            all_soups.append(BeautifulSoup(all_res[i]['response']['body'], 'lxml'))
        logger.debug('Returning list with all soups')
        return all_soups

    def urls_to_soups(self):
        logger.debug('Initializing urls_to_soups function')
        all_soups = self.get_soups(self.get_requests(self.post_requests()))
        return all_soups