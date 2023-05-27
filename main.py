import os
import sys
from src.logger import logging
from src.exception import CustomException

from src.scraper.index import Index
from src.scraper.page_list import PageList
from src.scraper.scraper import Scraper

from dotenv import load_dotenv
import time
import pandas as pd

from dataclasses import dataclass

@dataclass
class appConfig:
    urls = ['https://www.idealista.com/venta-viviendas/cornella-de-llobregat-barcelona/']
    urls_backup = [
        'https://www.idealista.com/venta-viviendas/cornella-de-llobregat-barcelona/',
        'https://www.idealista.com/venta-viviendas/barcelona/maresme/',
        'https://www.idealista.com/venta-viviendas/barcelona-barcelona/'
    ]

def main(): 
    start_time_ns = time.monotonic_ns()
    load_dotenv()
    logging.debug('###### Starting main program ######')
    
    for url in appConfig.urls:
        index = Index(url)
        index.get_all_breadcrumbs()

        logging.debug(f'New index was generated with name ''index-{index.name}.csv''')

        page_list = PageList(index.name)
        page_list.get_all_pagelists()

        scraper = Scraper(index.name)
        scraper.from_pagelists_get_data()

    logging.debug('###### Ending main program ######')
    end_time_ns = time.monotonic_ns()
    logging.debug(f'Time of execution: {pd.to_timedelta(end_time_ns - start_time_ns)}')

if __name__ == '__main__':
    main()