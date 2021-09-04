import configparser
from notion.client import NotionClient
import pandas as pd
from pandas.core.indexing import convert_from_missing_indexer_tuple

class CustomNotionClient():
    def __init__(self) -> None:
        config = configparser.ConfigParser()
        config.read('credentials.ini')

        self.client = NotionClient(token_v2=config.get("notion", "token"))
        self.cv = self.client.get_collection_view(config.get("notion", "database_url"))

    def __get_dicts_of_all_items(self) -> list:
        return [row.get_all_properties() for row in self.cv.collection.get_rows()]

    def convert_database_to_pandas(self):
        dataframe = pd.DataFrame(self.__get_dicts_of_all_items())
        dataframe['ablaufdatum'] = [None if time is None else time.start for time in dataframe['ablaufdatum']]
        return dataframe

    def get_names_of_available_products(self):
        names = [f"- {row.name}" for row in self.cv.collection.get_rows() if int(row.anzahl) > 0]
        return '\n'.join(names)

    def get_contents_as_string(self):
        self.convert_database_to_pandas()

def __main():
    notion_client = NotionClient()
    dataframe = notion_client.convert_database_to_pandas()
    dataframe.to_csv("test.csv")

if __name__ == '__main__':
    __main()