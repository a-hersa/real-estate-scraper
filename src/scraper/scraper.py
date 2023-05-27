import os
import sys
from src.logger import logging
from src.exception import CustomException

import pandas as pd
from src.scraper.scraperapi import Scraperapi
from src.scraper.scrapingant import Scrapingant
from datetime import date
from pathlib import Path
from src.mysql import mysqlObject, tablePageLists, tableProperties

class Scraper():
    def __init__(self, index_name):
        logging.info('Initializing Scraper class')
        self.index_name = index_name
        self.time = date.today()
        # pagelist_df = pd.read_csv(os.path.join(os.getcwd(),'data',f'{self.time.year}_{self.time.month:02d}-pagelist-{self.index_name}.csv'), header=None)
        pagelist_df = mysqlObject().getDfFromTable(tablePageLists, self.time.year, f'{self.time.month:02d}')
        self.index_list = pagelist_df.iloc[:, -1].values.tolist()

    def from_page_get_data(self, soup):
        logging.info('Initializing from_page_get_data function')
        row = []
        containers = soup.find_all('article', class_='item-multimedia-container')

        for container in containers:
            prop = container.find('div', class_='item-info-container')
            source = self.index_name
            id = prop.find('a', href=True, class_='item-link')['href'].split('/')[2]
            time = self.time
            title = prop.find('a', class_='item-link')['title']
            province = soup.find('div', class_='listing-top').ul.find_all('li')[1].a.text.strip('\n').replace(' provincia', '')
            breadcrumb_len = len(soup.find_all('li', class_='breadcrumb-navigation-element'))
            if breadcrumb_len > 2:
                county = soup.find_all('li', class_='breadcrumb-navigation-element')[2].span.text.strip('\n')
                if breadcrumb_len > 3:
                    city = soup.find_all('li', class_='breadcrumb-navigation-element')[3].span.text.strip('\n')
                    if breadcrumb_len > 4:
                        area = soup.find_all('li', class_='breadcrumb-navigation-element')[4].span.text.strip('\n')
                        if breadcrumb_len > 5:
                            neighborhood = soup.find_all('li', class_='breadcrumb-navigation-element')[5].span.text.strip('\n')
                        else:
                            neighborhood = 'None'
                    else:
                        area = 'None'
                        neighborhood = 'None'
                else:
                    city = 'None'
                    area = 'None'
                    neighborhood = 'None'
            else:
                county = 'None'
                city = 'None'
                area = 'None'
                neighborhood = 'None'
            prop_type = soup.find('link', rel='canonical')['href'].split('/')[3].split('-')[0]
            try:
                price = prop.find('span', class_='item-price h2-simulated').text.split('€', 1)[0].replace('.', '')
            except:
                price = None
            garage = ''
            try:
                if prop.find('span', class_='item-parking').text:
                    garage = 1
            except:
                garage = 0
            try:
                rooms = prop.find_all('span', class_='item-detail')[0].text[:-5]
                if rooms == '':
                    rooms = None
            except:
                rooms = None
            try:
                sqrm = ''.join(prop.find_all('span', class_='item-detail')[1].text[:-3].split('.'))
            except:
                sqrm = None
            try:
                if 'Planta' in prop.find_all('span', class_='item-detail')[2].text:
                    floor = prop.find_all('span', class_='item-detail')[2].text[7]
                elif 'Bajo' in prop.find_all('span', class_='item-detail')[2].text:
                    floor = '0'
                else:
                    floor = 'None'
            except:
                floor = 'None'
            try:
                if ('exterior' or 'interior') in prop.find_all('span', class_='item-detail')[2].text:
                    if 'exterior' in prop.find_all('span', class_='item-detail')[2].text:
                        surface = 'outdoor'
                    else:
                        surface = 'indoor'
                else:
                    surface = 'None'
            except:
                surface = 'None'
            try:
                if 'con ascensor' in prop.find_all('span', class_='item-detail')[2].text:
                    elevator = 1
                # elif 'sin ascensor' in prop.find_all('span', class_='item-detail')[2].text:
                #     elevator = 0
                else:
                    elevator = 0
            except:
                elevator = 0
            try:
                tag = prop.find('span', class_='listing-tags').text.strip('\n')
            except:
                tag = 'None'
            try:
                img = container.find_all('img')[1]['data-ondemand-img']
            except:
                img = 'None'
                pass
            url = 'https://www.idealista.com'+prop.find('a', href=True, class_='item-link')['href']
            row.append([source,id, time, province, county, city, area, neighborhood, title, prop_type, price, garage, rooms, sqrm, floor, surface, elevator, tag, img, url])
        logging.info('Returning data in a row')
        return row

    def from_pagelists_get_data(self):
        logging.info('Initializing from_pagelists_get_data function')
        df = pd.DataFrame(columns=['source','id', 'time', 'province', 'county', 'city', 'area', 'neighborhood', 'title', 'type', 'price', 'parking', 'rooms', 'sqrm', 'floor', 'surface', 'elevator', 'tag', 'img', 'url'], index=None)
        df.to_csv(os.path.join(os.getcwd(),'data',f'{self.time.year}_{self.time.month:02d}-data-{self.index_name}.csv'), mode='a', index=False)
        db = mysqlObject()
        for url in self.index_list:
            logging.info(f'loading soup for {url}')
            soup = Scrapingant(url).url_to_soup()
            df = pd.DataFrame(self.from_page_get_data(soup))
            df.to_csv(Path.cwd() / 'data' / f'{self.time.year}_{self.time.month:02d}-data-{self.index_name}.csv', mode='a', index=False, header=False)
            db.insertDfInTable(df,tableProperties)
            logging.info('line of data appended')
        logging.info(f'end of from_pagelists_get_data')