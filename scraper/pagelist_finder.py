import pandas as pd
import math
from scraper.scraperapi import Scraperapi
from datetime import date

class PageListFinder():
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
        one_pagelist = []
        total_props = self.total_props(soup)
        total_pag = self.total_pages(total_props)
        for i in range(total_pag):
            one_pagelist.append(self.url+f'pagina-{i+1}.htm')
        return one_pagelist
    
    def get_all_pagelists(self):
        all_pagelists = []
        for soup in self.soups:
            all_pagelists.append(self.get_pagelist(soup))
        return all_pagelists