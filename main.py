import re
import time
from contextlib import suppress
import requests as requests
from bs4 import BeautifulSoup
from lxml import html
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.common.by import By
from driver import get_options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as Ec
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
class Lazada:
    counter=2
    cs = service.Service(executable_path="driver/chromedriver.exe")
    options = get_options("testing1")
    driver = webdriver.ChromiumDriver(service=cs, browser_name="chrome", vendor_prefix="GC", options=options, )
    actions = ActionChains(driver)
    product_catagorey = input('Please enter your category:')
    product_catagoery_sub = input('Please enter your category_sub_type:')
    link=('https://www.lazada.com.my/shop-' + product_catagorey + '/' + product_catagoery_sub)
    driver.get(link)
    def page_links(self):
        last_Hieght = self.driver.execute_script('return document.body.scrollHeight')
        while True:
            self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            time.sleep(5)
            new_Hieght = self.driver.execute_script('return document.body.scrollHeight')
            if new_Hieght == last_Hieght:
                break
            last_Hieght = new_Hieght
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        links = soup.find_all('div', {'class': 'RfADt'})
        self.lst = []
        for i in links:
            ok = i.findNext('a').get('href')
            self.lst.append(ok)
        self.feature_scraping()
    def feature_scraping(self):
        actions = ActionChains(self.driver)
        for j in self.lst:
            try:
                self.driver.get('https:' + j)
                actions.scroll_to_element(self.driver.find_element(By.ID, 'module_product_detail')).perform()
                time.sleep(5)
                actions.scroll_to_element(self.driver.find_element(By.CLASS_NAME, 'pdp-product-detail')).perform()
                time.sleep(5)
                features_div = self.driver.execute_script(
                    'return document.getElementsByClassName("pdp-mod-specification")[0];')
                actions.scroll_to_element(features_div).perform()
                details = BeautifulSoup(self.driver.page_source, 'lxml')
                key_values = details.find('ul', {'class': 'specification-keys'})
                key_values_1 = key_values.find_all('li', {'class': 'key-li'})
                product_name = details.find('h1', {'class': 'pdp-mod-product-badge-title'}).text
                product_price = details.find('span', {
                    'class': 'pdp-price pdp-price_type_normal pdp-price_color_orange pdp-price_size_xl'}).text
                print('Product_Name:', product_name)
                print('Product_Price:', product_price)
                for k in key_values_1:
                    key = k.findNext('span', {'class': 'key-title'}).text
                    values = k.findNext('div', {'class': 'key-value'}).text
                    print(key, ':', values)
            except:
                pass
        self.next_page()
    def next_page(self):
        print('e3')
        self.driver.get(self.link + '/?page=' + str(self.counter))
        self.counter += 1
        self.page_links()
call=Lazada()
call.page_links()
