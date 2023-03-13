
import pandas as pd
import math
from scraper.scraperapi import Scraperapi
from scraper.scrapingant import Scrapingant
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s', '%Y-%m-%d %H:%M:%S')

file_handler = logging.FileHandler('scraper.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

class PageListFinder():
    def __init__(self, index_name):
        logger.debug('Initializing PageListFinder class')
        self.index_name = index_name.lower()
        index_df = pd.read_csv(f'data/index-{self.index_name}.csv', header=None)
        self.index_list = index_df.iloc[:, 0].values.tolist()
        scraper = Scrapingant(self.index_list)
        self.soups = scraper.urls_to_soups()
        # self.name = self.soup.find('link', rel='canonical')['href'].split('/')[-2]

    def total_props(self, soup):
        logger.debug('Initializing total_props function')
        total_props = int(''.join(soup.find('li', class_='breadcrumb-navigation-element inactive').find('span', class_='breadcrumb-navigation-element-info').text.split('.')))
        return total_props

    def total_pages(self, total_props):
        logger.debug('Initializing total_pages function')
        num_pages = total_props / 30
        if num_pages > 60:
            num_pages = 60
        return math.ceil(num_pages)

    def get_pagelist(self, soup):
        logger.debug('Initializing get_pagelist function')
        one_pagelist = []
        url = soup.find('link', rel='canonical')['href']
        one_pagelist.append(url)
        logger.debug(f'url appended {url}')
        total_props = self.total_props(soup)
        total_pag = self.total_pages(total_props)
        for i in range(total_pag-1):
            one_pagelist.append(url+f'pagina-{i+1}.htm')
            logger.debug(f'url appended {url}pagina-{i+1}.htm')
        logger.debug('Returning a list of resulting pagelists')
        return one_pagelist
    
    def get_all_pagelists(self):
        logger.debug('Initializing get_all_pagelists function')
        all_pagelists = []
        for soup in self.soups:
            all_pagelists.append(self.get_pagelist(soup))
        df = pd.DataFrame(all_pagelists)
        df.to_csv(f'data/pagelist-{self.index_name}.csv', index=False, header=False)
        logger.debug('Returning a list of all resulting pagelists')
        return all_pagelists