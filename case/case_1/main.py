import pandas as pd
import os

from datetime import datetime
from pages import TokopediaPage
from playwright.sync_api import sync_playwright
from re import IGNORECASE

def main(search_item:str, number_of_page:int) -> None:

    print(f"Process started for {search_item}")
    with sync_playwright() as playwright:
        timestamp = datetime.now().timestamp()

        print("Browser initiation (Headless)")
        # browser initiation
        browser = playwright.firefox.launch(headless=True)
        page = browser.new_page()

        try:
            # create new instance of TokopediaPage
            tokped = TokopediaPage(page)
            tokped.navigate()
            tokped.search(search_item)
            
            products = []
            # scrape data according to the number of page
            for x in range(number_of_page):
                print(f"Scraping page {x+1}")
                data = tokped.get_products_from_search()
                products.extend(data)

                print(f"Page {x+1} scraped!")
                # if this the end of pagination, stop
                if not tokped.next_search_page():
                    break
        except Exception as e:
            print(f"Process failed. Cause: {str(e)}")
            return
        finally:
            print("Closing browser")
            # close browser
            browser.close()

        # construct dataframe from scraped data
        df_product_data = pd.DataFrame(products)

        # export raw data to csv
        filename = f'{search_item}_raw_{timestamp}.csv'
        path = os.path.join('result', filename)
        df_product_data.to_csv(path, index=False)
        
        print("Post-processing started")
        # post-processing - transform raw price data to int
        # removing unwanted character or substring from the string and change the datatype after
        # should you need more char to be removed, just add to the price_pattern
        price_pattern = '|'.join(['Rp', '\.'])
        df_product_data['harga'] = df_product_data['harga'].str.replace(price_pattern, '', flags=IGNORECASE, regex=True).astype(int)

        # post-processing - transform raw sold item data to int
        # removing unwanted character or substring from the string
        # should you need more char to be removed, just add to the price_pattern
        sold_pattern = '|'.join(['\+','terjual'])
        df_product_data['jumlah_penjualan'] = df_product_data['jumlah_penjualan'].str.replace(sold_pattern,'', flags=IGNORECASE, regex=True)
        
        # replace the 'rb' to '000' as thousand and change the datatype to int
        df_product_data['jumlah_penjualan'] = df_product_data['jumlah_penjualan'].str.replace('rb', '000', flags=IGNORECASE, regex=True).astype(int)

        # calculate the GMV => harga * jumlah_penjualan
        df_product_data['estimasi_gmv'] = df_product_data['harga'] * df_product_data['jumlah_penjualan']

        # export the final result to csv
        filename = f'{search_item}_processed_{timestamp}.csv'
        path = os.path.join('result', filename)
        df_product_data.to_csv(path, index=False)

        print(f"Process {search_item} done. Files generated successfully.\n")
        return


if __name__ == '__main__':

    test_cases = [
        ('Rockbros', 1),
        ('Matoa', 5),
        ('konichiwa', 10)
    ]

    # iterate thru test cases
    for case in test_cases:
        main(*case)