from src.mysql import mysqlObject
from dotenv import load_dotenv

if __name__ == '__main__':
    load_dotenv()
    db = mysqlObject()
    db.createDatabase()
    db.createTables()
