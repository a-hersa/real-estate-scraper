import pandas as pd
import math
from scraper.scraperapi import Scraperapi
from datetime import date

class IndexScraper():
    def __init__(self, index_name):
        self.index_name = index_name.lower()
        index_df = pd.read_csv(f'data/index-{self.index_name}.csv', header=None)
        self.index_list = index_df.iloc[:, 0].values.tolist()
        scraperapi = Scraperapi(self.index_list)
        self.soups = scraperapi.urls_to_soups()
        # self.name = self.soup.find('link', rel='canonical')['href'].split('/')[-2]

    def total_props(self, soup):
        total_props = int(''.join(soup.find('li', class_='breadcrumb-navigation-element inactive').find('span', class_='breadcrumb-navigation-element-info').text.split('.')))
        return total_props

    def total_pages(self, total_props):
        num_pages = total_props / 30
        if num_pages > 60:
            num_pages = 60
        return math.ceil(num_pages)

    def get_pagelist(self, soup):
        pagelist = []
        total_props = self.total_props(soup)
        total_pag = self.total_pages(total_props)
        for i in range(total_pag):
            pagelist.append(self.url+f'pagina-{i+1}.htm')
        return pagelist
    
    def get_all_pagelists(self):
        scraping_list = []
        for soup in self.soups:
            scraping_list.append(self.get_pagelist(soup))
        return scraping_list
        
    def from_page_get_data(self, soup):
        data = []
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
            data.append([id, time, province, county, city, area, neighborhood, title, prop_type, price, garage, rooms, sqrm, floor, surface, elevator, tag, img, url])

        df = pd.DataFrame(data, columns = ['id', 'time', 'province', 'county', 'city', 'area', 'neighborhood', 'title', 'type', 'price', 'parking', 'rooms', 'sqrm', 'floor', 'surface', 'elevator', 'tag', 'img', 'url'], index=None)
        # save into csv
        df.to_csv('data/page-test.csv', index=False, encoding='utf-8')
        return df