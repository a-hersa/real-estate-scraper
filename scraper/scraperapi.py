
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
        self.url = url
    
    def post_request(self):
        r = requests.post(url = 'https://async.scraperapi.com/jobs', json={ 'apiKey': os.getenv('SCRAPERAPI_KEY'), 'url': self.url})
        status_url = json.loads(r.text)['statusUrl']
        return status_url
    
    def get_request(self, status_url):
        r = requests.get(url = status_url)
        res = json.loads(r.text)
        status = res['status']
        while status != 'finished':
            time.sleep(10)
            r = requests.get(url = status_url)
            res = json.loads(r.text)
            status = res['status']
        else:
            res = json.loads(r.text)
        return res

    def get_soup(self, res):
        soup = BeautifulSoup(res['response']['body'], 'lxml')
        return soup

    def url_to_soup(self):
        soup = self.get_soup(self.get_request(self.post_request()))
        return soup

    # Same methods for multiple requests
    def post_requests(self):
        r = requests.post(url = 'https://async.scraperapi.com/jobs', json={ 'apiKey': os.getenv('SCRAPERAPI_KEY'), 'urls': self.url})
        status_urls = []
        for i in range(len(self.url)):
            status_urls.append(json.loads(r.text)[i]['statusUrl'])
        return status_urls
    
    def get_requests(self, status_urls):
        all_res = []
        for i in range(len(status_urls)):
            time.sleep(30)
            r = requests.get(url = status_urls[i])
            res = json.loads(r.text)
            status = res['status']
            while status != 'finished':
                time.sleep(30)
                r = requests.get(url = status_urls[i])
                res = json.loads(r.text)
                status = res['status']
            else:
                all_res.append(json.loads(r.text))
        return all_res

    def get_soups(self, all_res):
        all_soups = []
        for i in range(len(all_res)):
            all_soups.append(BeautifulSoup(all_res[i]['response']['body'], 'lxml'))
        return all_soups

    def urls_to_soups(self):
        all_soups = self.get_soups(self.get_requests(self.post_requests()))
        return all_soups