# CASE STUDY 1
python version: `3.19.13`

dependencies: `requirements.txt`

target: [Tokopedia](http://tokopedia.com)

browser: `firefox`

required data:
- SKU
- price
- total sold
- page number
- GMV (price * total sold)


## summary
For this scenario I decided to use Playwright for its headless and faster execution.

The main execution and methods are contained in the `TokopediaPage`, a class made to wrap the base `Page` from Playwright. This approach makes the code more structured and easier to maintain.

The method used to scrape the data is called `get_products_from_search()`. This method only scrapes data from the active search page. Therefore, this class has `next_search_page()` and `previous_search_page()` methods in order to navigate the active page.

Tokopedia uses lazy loading to load the contents/products. The products become visible when users scroll the page down. For that reason, the `get_products_from_search()` method simulates the scrolling by creating a keyboard event. It will scroll until the navbar is visible, indicating the end of the container. It waits for 0.5 second after every keyboard press to give the page time to load its contents.

`get_products_from_search()` has two decorators. The `search_required` decorator indicates that the method only works after the `search()` method is executed, and the `timeout` decorator limits the runtime of the method to prevent an unresponsive process.

The data of each product is stored in a dictionary which will be collected in a list as the return of this method. This type of structure is convenient for multiple purposes for example inserting to database, or, in this case, transforming to `DataFrame`.

To maintain the *Single Responsibility Principle*, Post-processing happens outside of the `TokopediaPage` since it serves a different purpose.

The post-processing acts as data cleaning, the main purpose is to eliminate unwanted substring and transform it to the desired data type. The `replace()` method with `regex` could do the magic. 

After all, this program generates two CSV files for every search item, stored in result folder. The first file contains raw data and the second one contains processed data. The name format for each file is `{search_term}_raw_{timestamp}.csv` and `{search_term}_processed_{timestamp}.csv`.

The challenge I got while writing this program is ensuring the code is clean, maintainable, and easy to understand. Solving problem is one thing, but making sure everybody understands our code is a whole different challenge.


## Run
install dependencies
```sh
pip install -r requirements.txt
playwright install
```

run program
```sh
python main.py
```

## references
- [Playwright Doc](https://playwright.dev/python/)
- [Playwright Tutorial](https://youtube.com/playlist?list=PLYDwWPRvXB8_W56h2C1z5zrlnAlvqpJ6A&si=kbZnrBtV-fQlvSC_)
- [Timeout Decorator](https://www.saltycrane.com/blog/2010/04/using-python-timeout-decorator-uploading-s3/)