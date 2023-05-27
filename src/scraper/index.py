import os
import sys
from src.logger import logging
from src.exception import CustomException
from pathlib import Path

# from scraper.scraperapi import Scraperapi
from src.scraper.scrapingant import Scrapingant
from datetime import date
import pandas as pd
from src.mysql import mysqlObject, tableIndexes

class Index():
    def __init__(self, url):
        logging.info('Initializing IndexFinder class')
        self.url = url
        logging.info(f'len of self.url is {len(self.url)}')
        scraper = Scrapingant(self.url)
        self.soup = scraper.url_to_soup()
        self.name = self.soup.find('link', rel='canonical')['href'].split('/')[-2]
        logging.info(f'len of resulting self.soup is {len(self.soup)}')

    def get_depth(self):
        logging.info('Initializing get_depth function')
        page_depth = len(self.soup.find('ul', class_='breadcrumb-navigation').find_all('li', class_='breadcrumb-navigation-element'))
        return page_depth

    def get_breadcrumbs(self):
        logging.info('Initializing get_breadcrumbs function')
        breadcrumbs = []
        bc_list = self.soup.find('ul', 'breadcrumb-dropdown-subitem-list').find_all('li')
        for bc in bc_list:
            breadcrumbs.append('https://www.idealista.com' + bc.a['href'])
        logging.info('Returning a list of breadcrumbs')
        return breadcrumbs

    def get_all_breadcrumbs(self):
        logging.info('Initializing get_all_breadcrumbs function')
        depth = self.get_depth()
        bc_list = [[] for x in range(6-depth)]
        bc_list[0] = self.get_breadcrumbs()
        for i in range(len(bc_list)-1):
            to_remove = []
            for url in range(len(bc_list[i])):
                try:
                    upper_crumb = Index(bc_list[i][url])
                    lower_crumbs = upper_crumb.get_breadcrumbs()
                    for crumb in lower_crumbs:
                        bc_list[i+1].append(crumb)
                        logging.info(f'Lower crumbs added {crumb}')
                    to_remove.append(bc_list[i][url])
                except Exception:
                    logging.info(f'No lower crumbs found in {bc_list[i][url]}')
                    pass
            for x in range(len(to_remove)):
                bc_list[i].remove(to_remove[x])
                logging.info(f'url removed {to_remove[x]}')
        all_breadcrumbs = [url for sublist in bc_list for url in sublist]
        all_breadcrumbs2 = []
        if 'venta' in all_breadcrumbs[0]:
            for breadcrumb in all_breadcrumbs:
                all_breadcrumbs2.append(breadcrumb.replace('venta', 'alquiler'))
        else:
            for breadcrumb in all_breadcrumbs:
                all_breadcrumbs2.append(breadcrumb.replace('alquiler', 'venta'))
        joined_breadcrumbs = all_breadcrumbs + all_breadcrumbs2
        df = pd.DataFrame(joined_breadcrumbs, columns=['url'])
        time = date.today()
        df['date'] = str(time)
        df['source'] = self.name
        df = df[['source','date', 'url']]

        df.to_csv(Path.cwd() / 'data' / f'{time.year}_{time.month:02d}-index-{self.name}.csv', index=False, header=False)
        db = mysqlObject()
        db.insertDfInTable(df,tableIndexes)

        logging.info('Returning a list of breadcrumbs and saved them in a csv file')
        return joined_breadcrumbs