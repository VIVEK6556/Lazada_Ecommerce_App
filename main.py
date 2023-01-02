import re
import time
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
cs = service.Service(executable_path="driver/chromedriver.exe")
options = get_options("testing1")
driver = webdriver.ChromiumDriver(service=cs, browser_name="chrome", vendor_prefix="GC", options=options,)
actions = ActionChains(driver)
product_catagorey=input('Please enter your catagoery:')
product_catagoery_sub=input('Please enter your catagoery_sub_type:')
driver.get('https://www.lazada.com.my/shop-'+product_catagorey+'/'+product_catagoery_sub)
last_Hieght=driver.execute_script('return document.body.scrollHeight')
while True:
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    time.sleep(5)
    new_Hieght=driver.execute_script('return document.body.scrollHeight')
    if new_Hieght==last_Hieght:
        break
    last_Hieght=new_Hieght
soup = BeautifulSoup(driver.page_source, 'lxml')
links=soup.find_all('div',{'class':'RfADt'})
lst=[]
for i in links:
    ok=i.findNext('a').get('href')
    lst.append(ok)
actions = ActionChains(driver)
for j in lst:
    try:
        driver.get('https:'+j)
        actions.scroll_to_element(driver.find_element(By.ID, 'module_product_detail')).perform()
        time.sleep(5)
        actions.scroll_to_element(driver.find_element(By.CLASS_NAME, 'pdp-product-detail')).perform()
        time.sleep(5)
        features_div = driver.execute_script(
            'return document.getElementsByClassName("pdp-mod-specification")[0];')
        actions.scroll_to_element(features_div).perform()
        details=BeautifulSoup(driver.page_source,'lxml')
        key_values=details.find('ul',{'class':'specification-keys'})
        key_values_1=key_values.find_all('li',{'class':'key-li'})
        product_name = details.find('h1', {'class': 'pdp-mod-product-badge-title'}).text
        product_price = details.find('span', {
            'class': 'pdp-price pdp-price_type_normal pdp-price_color_orange pdp-price_size_xl'}).text
        print('Product_Name:', product_name)
        print('Product_Price:', product_price)
        for k in key_values_1:
            key=k.findNext('span',{'class':'key-title'}).text
            values=k.findNext('div',{'class':'key-value'}).text
            print(key,':',values)
    except:
        pass
