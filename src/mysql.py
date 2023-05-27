import os
import sys
import mysql.connector
from dataclasses import dataclass
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from src.utils import columnListForSQL

@dataclass
class tableIndexes:
    name = 'indexes'
    columns = 'source VARCHAR(255), date DATE, url VARCHAR(255)'
    column_list = ['source','date', 'url']

@dataclass
class tablePageLists:
    name = 'page_lists'
    columns = 'source VARCHAR(255), date DATE, url VARCHAR(255)'
    column_list = ['source','date', 'url']

@dataclass
class tableProperties:
    name = 'properties'
    columns = '''
        source VARCHAR(255),
        id INT(255),
        time DATE,
        province VARCHAR(255),
        county VARCHAR(255),
        city VARCHAR(255),
        area VARCHAR(255),
        neighborhood VARCHAR(255),
        title VARCHAR(255),
        type VARCHAR(255),
        price INT(255),
        parking INT(255),
        rooms INT(255),
        sqrm VARCHAR(255),
        floor VARCHAR(255),
        surface VARCHAR(255),
        elevator INT(255),
        tag VARCHAR(255),
        img VARCHAR(255),
        url VARCHAR(255)
    '''
    column_list = [
        'source',
        'id',
        'time',
        'province',
        'county',
        'city',
        'area',
        'neighborhood',
        'title',
        'type',
        'price',
        'parking',
        'rooms',
        'sqrm',
        'floor',
        'surface',
        'elevator',
        'tag',
        'img',
        'url'
    ]

class mysqlObject:
    def __init__(self):
        self.host:str = os.getenv('MYSQL_HOST')
        self.user:str = os.getenv('MYSQL_USER')
        self.passwd:str = os.getenv('MYSQL_PASSWD')
        self.db_name:str = os.getenv('MYSQL_DB_NAME')
        try:
            self.database = mysql.connector.connect(
                host = self.host,
                user = self.user,
                passwd = self.passwd,
                database = self.db_name
                )
            self.cursor = self.database.cursor()
        except Exception as e:
            logging.info('Couldnt connect to the mysql database')
            raise CustomException(e,sys)
        
    def createDatabase(self):
        try:
            self.database_no_db = mysql.connector.connect(
                host = self.host,
                user = self.user,
                passwd = self.passwd
                )
            self.cursor_no_db = self.database.cursor()
        except Exception as e:
            logging.info('Couldnt connect to the mysql database')
            raise CustomException(e,sys)
        self.cursor_no_db.execute(f'CREATE DATABASE IF NOT EXISTS {self.db_name}')

    def createTables(self):
        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {tableIndexes.name} ({tableIndexes.columns})')
        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {tablePageLists.name} ({tablePageLists.columns})')
        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {tableProperties.name} ({tableProperties.columns})')

    def insertRowInTable(self, row, table):
        cols = columnListForSQL(table.column_list)
        sql = f"INSERT INTO {table.name} ({cols}) VALUES ({'%s,'*(len(row)-1)} {'%s'})"
        self.cursor.execute(sql, tuple(row))
        # the connection is not autocommitted by default, so we must commit to save our # changes 
        self.database.commit()

    def insertDfInTable(self, df, table):
        for i,row in df.iterrows():
            self.insertRowInTable(row, table)

    def getDfFromTable(self, table, year, month):
        sql = f'SELECT * FROM {table.name} WHERE YEAR(date) = {year} AND MONTH(date) = {month}'
        self.cursor.execute(sql) # Fetch all the records
        df = pd.DataFrame(self.cursor.fetchall(), columns=table.column_list, index=None)
        return df