#!/usr/bin/env python
# coding: utf-8

# In[5]:


from selenium import webdriver
from bs4 import BeautifulSoup
import time
import requests
import pandas as pd

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support.expected_conditions import presence_of_element_located
# from selenium.common.exceptions import NoSuchElementException
# import string
# import openpyxl
# import os


# In[5]:


from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())


# In[6]:


driver.maximize_window()
url = 'https://www.google.com/maps/place/Zaman+Khan+Historical+Bridge/@32.4879082,50.8962974,17z/data=!4m7!3m6!1s0x3fbe591bb0638981:0x9e9ed6ee69e2994b!8m2!3d32.4879037!4d50.8984861!9m1!1b1?hl=en'
driver.get(url)


# In[7]:


#Find the total number of reviews
total_number_of_reviews = driver.find_element_by_xpath('//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[2]/div/div[2]/div[2]').text.split(" ")[0]
total_number_of_reviews = int(total_number_of_reviews.replace(',','')) if ',' in total_number_of_reviews else int(total_number_of_reviews)
#Find scroll layout
scrollable_div = driver.find_element_by_xpath('//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]')
#Scroll as many times as necessary to load all reviews
for i in range(0,(round(total_number_of_reviews/10-1))):
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
        time.sleep(5)


# In[8]:


response = BeautifulSoup(driver.page_source, 'html.parser')
reviews = response.find_all('div', class_='m6QErb DxyBCb kA9KIf dS8AEf')


# In[11]:



titles = []
stars = []
contents = []
title = response.find_all('div', {'class': 'd4r55'})
for t in title:
    ti = t.text
    titles.append(ti)

star = response.find_all('span', {'class': 'kvMYJc'})
for s in star:
    st = str(s).count('class="hCCjke vzX5Ic"')
    st = int(st)
    stars.append(st)
    
content = response.find_all('span', {'class': 'wiI7pd'})
for c in content:
    co = c.text
    contents.append(co)

rev = {'title': titles, 'star': stars, 'review': contents}
data = pd.DataFrame.from_dict(rev, orient='index')
data = data.transpose()
writer = pd.ExcelWriter('C:/Users/meisam/Desktop/heidary-reveiews.xlsx')
data.to_excel(writer)
writer.save()


# In[ ]:




