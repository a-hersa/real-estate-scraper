import os
import sys
from src.logger import logging
from src.exception import CustomException

import pandas as pd
import math
# from scraper.scraperapi import Scraperapi
from src.scraper.scrapingant import Scrapingant
from datetime import date
from pathlib import Path
import csv
from src.mysql import mysqlObject, tableIndexes, tablePageLists

class PageList():
    def __init__(self, index_name):
        logging.info('Initializing PageList class')
        self.index_name = index_name
        self.time = date.today()
        # index_df = pd.read_csv(os.path.join(os.getcwd(),'data',f'{self.time.year}_{self.time.month:02d}-index-{self.index_name}.csv'), header=None)
        index_df = mysqlObject().getDfFromTable(tableIndexes, self.time.year, f'{self.time.month:02d}')
        self.index_list = index_df.iloc[:, -1].values.tolist()

    def total_props(self, soup):
        logging.info('Initializing total_props function')
        try:
            total_props = int(''.join(soup.find('li', class_='breadcrumb-navigation-element inactive').find('span', class_='breadcrumb-navigation-element-info').text.split('.')))
        except Exception as e:
            logging.info('trying method 2 to get total_props...')
            total_props = int(soup.find_all('span', class_='breadcrumb-navigation-element-info')[2].text.split('\n')[1])
            raise CustomException(e,sys)
        return total_props

    def total_pages(self, total_props):
        logging.info('Initializing total_pages function')
        num_pages = total_props / 30
        if num_pages > 60:
            num_pages = 60
        return math.ceil(num_pages)

    def get_pagelist(self, soup):
        logging.info('Initializing get_pagelist function')
        one_pagelist = []
        url = soup.find('link', rel='canonical')['href']
        one_pagelist.append(url)
        logging.info(f'url appended {url}')
        total_props = self.total_props(soup)
        total_pag = self.total_pages(total_props)
        for i in range(1, total_pag):
            one_pagelist.append(url+f'pagina-{i+1}.htm')
            logging.info(f'url appended {url}pagina-{i+1}.htm')
        logging.info('Returning a list of resulting pagelists')
        return one_pagelist
    
    def get_all_pagelists(self):
        logging.info('Initializing get_all_pagelists function')
        all_pagelists = []
        for index in self.index_list:
            # pagelist = []
            logging.info(f'loading soup for {index}')
            soup = Scrapingant(index).url_to_soup()
            single_list = self.get_pagelist(soup)
            logging.info(f'printing list to append {single_list}')
            for page in single_list:
                all_pagelists.append(page)
            with open(Path.cwd() / 'data' / f'{self.time.year}_{self.time.month:02d}-pagelist-{self.index_name}.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter='\n')
                writer.writerow(single_list)
        df = pd.DataFrame(all_pagelists, columns=['url'])
        time = date.today()
        df['date'] = str(time)
        df['source'] = self.index_name
        df = df[['source','date', 'url']]
        db = mysqlObject()
        db.insertDfInTable(df,tablePageLists)
        logging.info('Returning a list of all resulting pagelists')
        return all_pagelists