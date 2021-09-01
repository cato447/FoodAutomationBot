import configparser

from notion.client import *
from notion.collection import NotionDate

import pandas as pd

def main():
    config = configparser.ConfigParser()
    config.read('credentials.ini')

    client = NotionClient(token_v2=config.get("notion", "token"))

    # Access a database using the URL of the database page or the inline block
    cv = client.get_collection_view(config.get("notion", "database_url"))

    print(get_all_available_items(cv))

def get_all_available_items(cv):
    return [row.name for row in cv.collection.get_rows() if int(row.anzahl) > 0]

if __name__ == '__main__':
    main()