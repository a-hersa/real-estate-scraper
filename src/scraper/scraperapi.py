import os
from src.logger import logging

import requests
from bs4 import BeautifulSoup
import json
import time

class Scraperapi():
    def __init__(self, url):
        logging.info('Initializing Scraperapi class')
        self.url = url
    
    def post_request(self):
        logging.info('Initializing post_request function')
        r = requests.post(url = 'https://async.scraperapi.com/jobs', json={ 'apiKey': os.getenv('SCRAPERAPI_KEY1'), 'url': self.url})
        status_url = json.loads(r.text)['statusUrl']
        logging.info(f'Returning {status_url}')
        return status_url
    
    def get_request(self, status_url):
        logging.info('Initializing get_request function')
        r = requests.get(url = status_url)
        res = json.loads(r.text)
        status = res['status']
        while status != 'finished':
            logging.info('Waiting 30 secs...')
            time.sleep(30)
            r = requests.get(url = status_url)
            res = json.loads(r.text)
            status = res['status']
        else:
            res = json.loads(r.text)
        logging.info('Returning response')
        return res

    def get_soup(self, res):
        logging.info('Initializing get_soup function')
        soup = BeautifulSoup(res['response']['body'], 'lxml')
        logging.info('Returning soup')
        return soup

    def url_to_soup(self):
        logging.info('Initializing url_to_soup function')
        soup = self.get_soup(self.get_request(self.post_request()))
        return soup

    # Same methods for multiple requests
    def post_requests(self):
        logging.info('Initializing post_requests function')
        r = requests.post(url = 'https://async.scraperapi.com/jobs', json={ 'apiKey': os.getenv('SCRAPERAPI_KEY1'), 'urls': self.url})
        status_urls = []
        for i in range(len(self.url)):
            status_urls.append(json.loads(r.text)[i]['statusUrl'])
        logging.info('Returning list of status_urls')
        for url in status_urls:
            logging.info(url)
        return status_urls
    
    def get_requests(self, status_urls):
        logging.info('Initializing get_requests function')
        all_res = []
        for i in range(len(status_urls)):
            logging.info('Waiting 30 secs...')
            time.sleep(30)
            r = requests.get(url = status_urls[i])
            res = json.loads(r.text)
            status = res['status']
            while status != 'finished':
                logging.info('Waiting 30 secs...')
                time.sleep(30)
                r = requests.get(url = status_urls[i])
                res = json.loads(r.text)
                status = res['status']
            else:
                all_res.append(json.loads(r.text))
        logging.info('Returning list with all rersponses')
        return all_res

    def get_soups(self, all_res):
        logging.info('Initializing get_soups function')
        all_soups = []
        for i in range(len(all_res)):
            all_soups.append(BeautifulSoup(all_res[i]['response']['body'], 'lxml'))
        logging.info('Returning list with all soups')
        return all_soups

    def urls_to_soups(self):
        logging.info('Initializing urls_to_soups function')
        all_soups = self.get_soups(self.get_requests(self.post_requests()))
        return all_soups