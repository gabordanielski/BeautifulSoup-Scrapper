import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

__author__ = "Gabor Danielski"
__version__ = "0.1.0"
__version_upload_date__ = "05.03.2021"

BASE_URL = 'https://www.ebay.com/deals'
OUTPUT_FILE = 'output.csv'


class Scrapper:
    def __init__(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return

    def get_data(self):
        page = requests.get(BASE_URL)
        df = pd.DataFrame(
            columns=['Item', 'Current_ price', 'Previous_price', 'Image_name'])

        soup = BeautifulSoup(page.content, 'html.parser')
        items = soup.find_all('div', class_="dne-itemtile")

        for i in items:

            row = []

            # Item name
            name = i.find('span').find('span').text
            if name != 'Show':
                row.append(name)
            else:
                continue

            # Item current price
            current_price = i.find('div', class_='dne-itemtile-detail').find('div').find('span').text
            if '$' in current_price:
                row.append(current_price)
            else:
                row.append(np.nan)

            # Previous_price, Image_name fields
            row.append(np.nan)
            row.append(np.nan)

            if len(row) > 1:
                s = pd.Series(row, index=['Item', 'Current_ price', 'Previous_price', 'Image_name'])
                df = df.append(s, ignore_index=True)

        print(df.head())
        print(df.shape)
        df.to_csv('output/' + OUTPUT_FILE)


if __name__ == '__main__':
    with Scrapper() as scrapper:
        scrapper.get_data()
