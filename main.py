import configparser
from notion.client import NotionClient
import pandas as pd
from pprint import pprint

def get_dicts_of_all_items(cv) -> list:
    return [row.get_all_properties() for row in cv.collection.get_rows()]

def convert_database_to_pandas(cv):
    dataframe = pd.DataFrame(get_dicts_of_all_items(cv))
    dataframe['ablaufdatum'] = [None if time is None else time.start for time in dataframe['ablaufdatum']]
    return dataframe

def main():
    config = configparser.ConfigParser()
    config.read('credentials.ini')

    client = NotionClient(token_v2=config.get("notion", "token"))

    # Access a database using the URL of the database page or the inline block
    cv = client.get_collection_view(config.get("notion", "database_url"))
    dataframe = convert_database_to_pandas(cv)
    dataframe.to_csv("test.csv")

if __name__ == '__main__':
    main()