
from scraper.index_finder import IndexFinder
from scraper.pagelist_finder import PageListFinder
from scraper.scraper import Scraper
from os import path
import logging
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s', '%Y-%m-%d %H:%M:%S')

file_handler = logging.FileHandler('scraper.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

def configure():
    load_dotenv()

def main():
    configure()
    logger.debug('###### Starting main program ######')

    url = 'https://www.idealista.com/venta-viviendas/barcelona/maresme/'
    logger.debug(f'URL added {url}')
    
    index_list = IndexFinder(url)
    if path.exists(f'data/index-{index_list.name}.csv'):
        logger.debug(f'Index for {index_list.name} already exists, skipping...')
        pass
    else:
        index_list.get_all_breadcrumbs()
        logger.debug(f'New index was generated with name ''index-{index.name}.csv''')
    
    page_list = PageListFinder(index_list.name)
    page_list.get_all_pagelists()

    scraper = Scraper(index_list.name)
    scraper.from_pagelists_get_data()

    logger.debug('###### Ending main program ######')
    

if __name__ == '__main__':
    main()