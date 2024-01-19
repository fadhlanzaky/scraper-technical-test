import time

from functools import wraps
from playwright.sync_api import Page, Locator
from util import timeout

class TokopediaPage:
    def __init__(self, page: Page):
        # initiate page
        self.page = page
        self.search_state = False

        # DOM elements
        self.search_product_container = 'div[data-ssr="contentProductsSRPSSR"][data-testid="divSRPContentProducts"]'
        self.search_product_card = 'div[data-testid="master-product-card"] .prd_container-card .pcv3__container'
        self.search_nav_bar = 'nav[aria-label="Navigasi laman"]'
        self.search_nav_bar_wrapper = '.css-gvoll6'
    

    def navigate(self):
        # navigate to tokopedia
        self.page.goto('http://www.tokopedia.com')


    def search(self, item: str):
        # locate the search bar and start searching
        search_bar = self.page.locator('input[type="search"]')
        search_bar.fill(item)
        search_bar.press('Enter')

        # wait until the main product container visible
        self.page.wait_for_selector(self.search_product_container)
        self.search_state = True


    def search_required(func):
        # this decorator checks the state of the page
        # some of the methods are required to be executed in search state
        # hence this decorator
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not self.search_state:
                raise AssertionError('This method only works in search state') 
            return func(self, *args, **kwargs)
        return wrapper


    @search_required
    # only turn this on if executed on Linux/UNIX
    # @timeout(180) # some process took longer to process hence the timeout decorator
    def get_products_from_search(self) -> list:
        products = []

        # emulate user scroll to trigger lazy loading
        while self.page.locator(self.search_nav_bar).count() < 1:
            self.page.keyboard.press('PageDown')
            time.sleep(0.5)

        page = self.get_search_page_number()

        # locate all product cards
        container = self.page.locator(self.search_product_container)
        product_cards = container.locator(self.search_product_card).all()
        
        # iterate thru all cards and retrieve the required data
        for card in product_cards:
            product = {
                'nama_sku': card.locator('.prd_link-product-name').text_content(),
                'harga': card.locator('.prd_link-product-price').text_content(),
                'jumlah_penjualan': ('0' if card.locator('.prd_label-integrity').count() == 0 
                                     else card.locator('.prd_label-integrity').text_content()),
                'halaman': page
            }

            products.append(product)
        
        return products
    

    @search_required
    def get_search_page_number(self) -> int:
        navbar = self.__get_navbar()
        page_no = navbar.locator('ul li button[data-active="true"]').inner_text()
        return page_no


    # move to the next page
    @search_required
    def next_search_page(self) -> bool:
        navbar = self.__get_navbar()
        next_page_button = navbar.locator('button[aria-label="Laman berikutnya"]')

        # return False if it's at the end of the pagination, else True
        if not next_page_button.is_disabled():
            next_page_button.click()
            self.page.wait_for_selector(self.search_product_container)
            return True
        else:
            return False
        
    
    # move to the previous page
    @search_required
    def previous_search_page(self) -> bool:
        navbar = self.__get_navbar()
        prev_page_button = navbar.locator('button[aria-label="Laman sebelumnya"]')

        # return False if it's at the start of the pagination, else True
        if not prev_page_button.is_disabled():
            prev_page_button.click()
            self.page.wait_for_selector(self.search_product_container)
            return True
        else:
            return False
        
    # private method to get the navbar
    @search_required
    def __get_navbar(self) -> Locator:
        if self.page.locator(self.search_nav_bar).count() < 1:
            self.page.locator(self.search_nav_bar_wrapper).scroll_into_view_if_needed()
            self.page.wait_for_selector(self.search_nav_bar)
        
        return self.page.locator(self.search_nav_bar)