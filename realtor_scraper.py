# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 12:45:53 2021

@author: peter
"""

import requests
import time
from bs4 import BeautifulSoup
import random

headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'referrer': 'https://www.google.com/',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Pragma': 'no-cache',
    }

delays = [7, 4, 6, 2, 10, 19]

b_valid_page = True
b_page = 1
b_count = 0
b_total_price = 0
b_total_sqft = 0
b_bot = False

while b_valid_page == True:
    url = 'https://www.realtor.com/realestateandhomes-search/78412/type-single-family-home/pg-%d' % b_page
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")
    no_houses_query = soup.find_all('div', attrs={'id': 'error-404'})
    for each in no_houses_query:
        if "Sorry" in each.text.strip():
            b_valid_page = False
    bot_query = soup.find_all('p')
    for each in bot_query:
        if "bot" in each.text.strip():
            print("It thinks you're a bot")
            b_bot = True
    if b_bot == True:
        break
    if b_valid_page == True:
        b_house_price = soup.find_all('span', attrs={'data-label': 'pc-price'})
        b_sqft = soup.find_all('li', attrs={'data-label': 'pc-meta-sqft'})
        for p, s in zip(b_house_price, b_sqft):
            b_count += 1
            b_total_price += int(p.text.replace("$","").replace(",","").replace("From",""))
            b_total_sqft += int(s.text.replace(",","").replace("sqft",""))
        b_page += 1
        print(b_page)
        time.sleep(random.choice(delays))
    
price_per_sqft = int(b_total_price/b_total_sqft)

print("Average house price: ", int(b_total_price/b_count), "Average $/sqft: ", int(b_total_price/b_total_sqft))



r_valid_page = True
r_page = 1
r_count = 0
r_total_rent = 0
r_total_sqft = 0
r_bot = False

while r_valid_page == True:
    url = 'https://www.realtor.com/apartments/78412/type-single-family-home/pg-%d' % r_page
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")
    no_houses_query = soup.find_all('div', attrs={'id': 'error-404'})
    for each in no_houses_query:
        if "Sorry" in each.text.strip():
            r_valid_page = False
    bot_query = soup.find_all('p')
    for each in bot_query:
        if "bot" in each.text.strip():
            print("It thinks you're a bot")
            r_bot = True
    if r_bot == True:
        break
    if r_valid_page == True:
        r_rental_price = soup.find_all('span', attrs={'data-label': 'pc-price'})
        r_sqft = soup.find_all('li', attrs={'data-label': 'pc-meta-sqft'})
        for p, s in zip(r_rental_price, r_sqft):
            r_count += 1
            r_total_rent += int(p.text.replace("$","").replace(" /month","").replace(",","").replace("+",""))
            r_total_sqft += int(s.text.replace(",","").replace("sqft",""))
        r_page += 1
        print(r_page)
        time.sleep(random.choice(delays))

rent_per_sqft = int(r_total_rent/r_total_sqft)

print("Average rental price: ", int(r_total_rent/r_count), "Average $/sqft: ", (r_total_rent/r_total_sqft))

print("The ratio of average house $/sqft to average monthly rental $/sqft is: ", int(price_per_sqft/rent_per_sqft))


 
















