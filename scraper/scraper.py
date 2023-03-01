
import pandas as pd
from scraper.scraperapi import Scraperapi
from scraper.scrapingant import Scrapingant
from datetime import date
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s', '%Y-%m-%d %H:%M:%S')

file_handler = logging.FileHandler('scraper.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

class Scraper():
    def __init__(self, index_name):
        logger.debug('Initializing Scraper class')
        self.index_name = index_name.lower()
        pagelist_df = pd.read_csv(f'data/pagelist-{self.index_name}.csv', header=None)
        self.index_list = pagelist_df.iloc[:, 0].values.tolist()
        scraper = Scrapingant(self.index_list)
        self.soups = scraper.urls_to_soups()

    def from_page_get_data(self, soup):
        logger.debug('Initializing from_page_get_data function')
        row = []
        containers = soup.find_all('article', class_='item_contains_branding')

        for container in containers:
            property = container.find('div', class_='item-info-container')
            id = property.find('a', href=True, class_='item-link')['href'].split('/')[2]
            time = date.today()
            title = property.find('a', class_='item-link')['title']
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
            price = ''.join(property.find('span', class_='item-price h2-simulated').text[:-1].split('.'))
            garage = ''
            try:
                if property.find('span', class_='item-parking').text:
                    garage = 1
            except:
                garage = 0
            rooms = property.find_all('span', class_='item-detail')[0].text[:-5]
            sqrm = ''.join(property.find_all('span', class_='item-detail')[1].text[:-3].split('.'))
            try:
                if 'Planta' in property.find_all('span', class_='item-detail')[2].text:
                    floor = property.find_all('span', class_='item-detail')[2].text[7]
                elif 'Bajo' in property.find_all('span', class_='item-detail')[2].text:
                    floor = '0'
                else:
                    floor = 'None'
            except:
                floor = 'None'
            try:
                if ('exterior' or 'interior') in property.find_all('span', class_='item-detail')[2].text:
                    if 'exterior' in property.find_all('span', class_='item-detail')[2].text:
                        surface = 'outdoor'
                    else:
                        surface = 'indoor'
                else:
                    surface = 'None'
            except:
                surface = 'None'
            try:
                if 'con ascensor' in property.find_all('span', class_='item-detail')[2].text:
                    elevator = 1
                elif 'sin ascensor' in property.find_all('span', class_='item-detail')[2].text:
                    elevator = 0
                else:
                    elevator = 'None'
            except:
                elevator = 'None'
            try:
                tag = property.find('span', class_='listing-tags').text.strip('\n')
            except:
                tag = 'None'
            img = container.find('img', alt="")['data-ondemand-img']
            url = 'https://www.idealista.com'+property.find('a', href=True, class_='item-link')['href']
            row.append([id, time, province, county, city, area, neighborhood, title, prop_type, price, garage, rooms, sqrm, floor, surface, elevator, tag, img, url])

        # save into csv
        # df.to_csv('data/page-test.csv', index=False, encoding='utf-8')
        logger.debug('Returning data in a row')
        return row

    def from_pagelists_get_data(self):
        logger.debug('Initializing from_pagelists_get_data function')
        df = pd.DataFrame(columns=['id', 'time', 'province', 'county', 'city', 'area', 'neighborhood', 'title', 'type', 'price', 'parking', 'rooms', 'sqrm', 'floor', 'surface', 'elevator', 'tag', 'img', 'url'], index=None)
        for soup in self.soups:
            df.loc[len(df)] = self.from_page_get_data(soup)
        df.to_csv(f'data/data-{self.index_name}.csv', index=False, header=False)
        return df