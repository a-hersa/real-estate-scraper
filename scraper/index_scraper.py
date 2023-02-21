import pandas as pd
import math
from scraper.scraperapi import Scraperapi
from datetime import datetime

class IndexScraper():
    def __init__(self, url):
        self.url = url
        scraperapi = Scraperapi(self.url)
        self.soup = scraperapi.url_to_soup()
        self.name = self.soup.find('link', rel='canonical')['href'].split('/')[-2]

    def total_props(self):
        total_props = int(''.join(self.soup.find('li', class_='breadcrumb-navigation-element inactive').find('span', class_='breadcrumb-navigation-element-info').text.split('.')))
        return total_props

    def total_pages(self, total_props):
        num_pages = total_props / 30
        if num_pages > 60:
            num_pages = 60
        return math.ceil(num_pages)

    def get_pagelist(self):
        pagelist = []
        total = self.total_props()
        total_pag = self.total_pages(total)
        for i in range(total_pag):
            pagelist.append(self.url+f'pagina-{i+1}.htm')
        return pagelist

    def from_page_get_data(self, soup):
        data = []
        containers = soup.find_all('article', class_='item_contains_branding')
        properties = soup.find_all('div', class_='item-info-container')

        for property in properties:
            id = property.find('a', href=True, class_='item-link')['href'].split('/')[2]
            time = datetime.now()
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
                            neighborhood = 'none'
                    else:
                        area = 'none'
                        neighborhood = 'none'
                else:
                    city = 'none'
                    area = 'none'
                    neighborhood = 'none'
            else:
                county = 'none'
                city = 'none'
                area = 'none'
                neighborhood = 'none'
            prop_type = 'sell'
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
                tag = property.find('span', class_='listing-tags').text.strip('\n')
            except:
                tag = 'none'
            url = 'https://www.idealista.com'+property.find('a', href=True, class_='item-link')['href']
            data.append([id, time, province, county, city, area, neighborhood, title, prop_type, price, garage, rooms, sqrm, tag, url])

        df = pd.DataFrame(data, columns = ['id', 'time', 'province', 'county', 'city', 'area', 'neighborhood', 'title', 'type', 'price', 'parking', 'rooms', 'sqrm', 'tag', 'url'], index=None)
        # save into csv
        # df.to_csv('data/listing-test2.csv', index=False, encoding='utf-8')
        return df