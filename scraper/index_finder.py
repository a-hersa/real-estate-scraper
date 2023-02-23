from scraper.scraperapi import Scraperapi
import pandas as pd

class IndexFinder():
    def __init__(self, url):
        self.url = url
        scraperapi = Scraperapi(self.url)
        if type(self.url) is str:
            self.soup = scraperapi.url_to_soup()
        else:
            self.soup = scraperapi.urls_to_soups()
        self.name = self.soup.find('link', rel='canonical')['href'].split('/')[-2]

    def get_depth(self):
        page_depth = len(self.soup.find('ul', class_='breadcrumb-navigation').find_all('li', class_='breadcrumb-navigation-element'))
        return page_depth

    def get_breadcrumbs(self):
        breadcrumbs = []
        bc_list = self.soup.find('ul', 'breadcrumb-dropdown-subitem-list').find_all('li')
        for bc in bc_list:
            breadcrumbs.append('https://www.idealista.com' + bc.a['href'])
        return breadcrumbs

    def get_breadcrumbs_from_list(self, old_list):
        breadcrumbs = []
        for bc in self.soup:
            try:
                bc_list = bc.find('ul', 'breadcrumb-dropdown-subitem-list').find_all('li')
                old_url = bc.find('link', rel='canonical')['href']
                old_list.remove(old_url)
                for crumb in bc_list:
                    breadcrumbs.append('https://www.idealista.com' + crumb.a['href'])
            except:
                pass
        return breadcrumbs 

    def get_all_breadcrumbs(self):
        depth = self.get_depth()
        bc_list = [[] for x in range(6-depth)]
        bc_list[0] = self.get_breadcrumbs()
        while depth <= 6:
            for i in range(len(bc_list)):
                try:
                    upper_crumbs = IndexFinder(bc_list[i])
                    lower_crumbs = upper_crumbs.get_breadcrumbs_from_list(bc_list[i])
                    for crumb in lower_crumbs:
                        bc_list[i+1].append(crumb)
                except Exception:
                    print('1 url without breadcrumbs reached')
                    pass
            depth += 1
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
        return all_breadcrumbs