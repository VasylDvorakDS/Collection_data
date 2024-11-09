# Парсинг HTML. BeautifulSoup

## Выполнить скрейпинг данных в веб-сайта http://books.toscrape.com/ и
## извлечь информацию о всех книгах на сайте во всех категориях: название,
## цену, количество товара в наличии (In stock (19 available)) в формате integer,
## описание.
## Затем сохранить эту информацию в JSON-файле

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from sympy import pprint
import re
import pandas as pd
import time

item=1

url='http://books.toscrape.com/'
ua=UserAgent().random
header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

session=requests.session()
response=session.get(url, headers=header, timeout=1)
soup=BeautifulSoup(response.text,"html.parser")

books=[]
categories_list=[]
categories_list_prime=soup.find('ul',{'class', 'nav nav-list'}).find_all('li')

for cat in categories_list_prime:
    category={}
    category['title_category'] =  cat.find('a').get_text(strip=True)
    category['link_categories'] = url + cat.find('a').get('href')
    categories_list.append(category)
categories_list.pop(0)

for cat_item in categories_list:
    next_page=cat_item['link_categories']
    while True:
        time.sleep(1)
        response_for_cat_item = session.get(next_page, headers=header, timeout=1)
        soup_for_cat_item = BeautifulSoup(response_for_cat_item.content, 'html.parser')
        banners_books=soup_for_cat_item.find_all('article', {'class': 'product_pod'})

        for banner_book in banners_books:
            book={}
            area_cont = banner_book.findChildren()[0]
            book['Category']= cat_item['title_category']
            book['Link'] = url+'catalogue/'+area_cont.find('a').get('href')[8:]
            book['Name'] = area_cont.find('img').get('alt')
            book['Price'] = banner_book.find('p', {'class': 'price_color'}).getText()[1:]
            time.sleep(1)
            response_for_book=session.get(book['Link'], headers=header, timeout=1)
            soup_for_book = BeautifulSoup(response_for_book.content, 'html.parser')
            page_book_info = soup_for_book.find('div', {'class': 'page_inner'})
            book['In_stock']=soup_for_book.find('p', {'class': 'instock availability'}).get_text(strip=True)
            number=re.search(r'\d+', book['In_stock']).group()
            book['In_stock_available'] =int(number if number else 0)
            book['Description'] = soup_for_book.find('article', {'class': 'product_page'}).findAll('p')[-1].getText()
            books.append(book)
            print('Вытащили информацию о книге: ', book['Name'],' #', item)
            item += 1

        next_button=soup_for_cat_item.find('a', string='next')
        if not next_button:
            break
        next_page=next_page[:next_page.rfind('/')+1]+next_button.get('href')

print('Все данные о книгах вытащены, всег книг: ', len(books))

category=[]
name=[]
price=[]
in_stock=[]
in_stock_available=[]
description=[]
link=[]

for book in books:
    category.append(book['Category'])
    name.append(book['Name'])
    price.append(book['Price'])
    in_stock.append(book['In_stock'])
    in_stock_available.append(book['In_stock_available'])
    description.append(book['Description'])
    link.append(book['Link'])


formatted_library = {'Category' : category, 'Name' : name, 'Price' : price, 'In_stock' : in_stock,
                     'In_stock_available' : in_stock_available, 'Description' : description, 'Link' : link}

df = pd.DataFrame(formatted_library)

# Преобразуем DataFrame в JSON файл
df.to_json('books_library.json', orient='records', lines=True)
print("Данные о книгах записаны в JSON file  'books_library.json'\n \n")
print('Окончательный DataFrame всех книг:')
print(df)


