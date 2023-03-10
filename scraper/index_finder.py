
from scraper.scraperapi import Scraperapi
from scraper.scrapingant import Scrapingant
import pandas as pd
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s', '%Y-%m-%d %H:%M:%S')

file_handler = logging.FileHandler('scraper.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

class IndexFinder():
    def __init__(self, url):
        logger.debug('Initializing IndexFinder class')
        self.url = url
        logger.debug(f'len of self.url is {len(self.url)}')
        scraper = Scrapingant(self.url)
        if type(self.url) is str:
            self.soup = scraper.url_to_soup()
            self.name = self.soup.find('link', rel='canonical')['href'].split('/')[-2]
        else:
            self.soup = scraper.urls_to_soups()
            self.name = []
            for soup in self.soup:
                self.name.append(soup.find('link', rel='canonical')['href'].split('/')[-2])
        logger.debug(f'len of resulting self.soup is {len(self.soup)}')
        # self.name = self.soup.find('link', rel='canonical')['href'].split('/')[-2]

    def get_depth(self):
        logger.debug('Initializing get_depth function')
        page_depth = len(self.soup.find('ul', class_='breadcrumb-navigation').find_all('li', class_='breadcrumb-navigation-element'))
        return page_depth

    def get_breadcrumbs(self):
        logger.debug('Initializing get_breadcrumbs function')
        breadcrumbs = []
        bc_list = self.soup.find('ul', 'breadcrumb-dropdown-subitem-list').find_all('li')
        for bc in bc_list:
            breadcrumbs.append('https://www.idealista.com' + bc.a['href'])
        logger.debug('Returning a list of breadcrumbs')
        return breadcrumbs

    def get_breadcrumbs_from_list(self, old_list):
        logger.debug('Initializing get_breadcrumbs_from_list function')
        breadcrumbs = []
        # df = pd.DataFrame(self.soup)
        # df.to_csv(f'data/get_breadcrumbs_from_list.csv', index=False, header=False)
        for bc in self.soup:
            try:
                bc_list = bc.find('ul', 'breadcrumb-dropdown-subitem-list').find_all('li')
                old_url = bc.find('link', rel='canonical')['href']
                # old_list.remove(old_url)
                for crumb in bc_list:
                    breadcrumbs.append('https://www.idealista.com' + crumb.a['href'])
            except Exception as e:
                logger.exception(f'Exception occurred: {e}')
        logger.debug('Returning a list of breadcrumbs')
        return breadcrumbs 

    def get_all_breadcrumbs(self):
        logger.debug('Initializing get_all_breadcrumbs function')
        depth = self.get_depth()
        bc_list = [[] for x in range(6-depth)]
        bc_list[0] = self.get_breadcrumbs()
        for i in range(len(bc_list)-1):
            to_remove = []
            for url in range(len(bc_list[i])):
                try:
                    upper_crumb = IndexFinder(bc_list[i][url])
                    lower_crumbs = upper_crumb.get_breadcrumbs()
                    for crumb in lower_crumbs:
                        bc_list[i+1].append(crumb)
                        logger.debug(f'Lower crumbs added {crumb}')
                    to_remove.append(bc_list[i][url])
                except Exception:
                    logger.debug(f'No lower crumbs found in {bc_list[i][url]}')
                    pass
            for x in range(len(to_remove)):
                bc_list[i].remove(to_remove[x])
                logger.debug(f'url removed {to_remove[x]}')
        all_breadcrumbs = [url for sublist in bc_list for url in sublist]
        all_breadcrumbs2 = []
        if 'venta' in all_breadcrumbs[0]:
            for breadcrumb in all_breadcrumbs:
                all_breadcrumbs2.append(breadcrumb.replace('venta', 'alquiler'))
        else:
            for breadcrumb in all_breadcrumbs:
                all_breadcrumbs2.append(breadcrumb.replace('alquiler', 'venta'))
        joined_breadcrumbs = all_breadcrumbs + all_breadcrumbs2
        df = pd.DataFrame(joined_breadcrumbs)
        df.to_csv(f'data/index-{self.name}.csv', index=False, header=False)
        logger.debug('Returning a list of breadcrumbs and saved them in a csv file')
        return joined_breadcrumbs