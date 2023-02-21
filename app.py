# import requests
# from bs4 import BeautifulSoup
# import pandas as pd
# import json
# import time
# import math
from scraper.index_finder import IndexFinder
from dotenv import load_dotenv

def configure():
    load_dotenv()

def main():
    configure()
    print('configured')
    url = 'https://www.idealista.com/venta-viviendas/barcelona/maresme/'
    print('url added')
    maresme = IndexFinder(url)
    print('class created')
    maresme.get_all_breadcrumbs()
    print('breadcrumbs found')

if __name__ == '__main__':
    main()