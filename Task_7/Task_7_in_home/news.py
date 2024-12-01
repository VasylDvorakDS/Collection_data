from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pprint import pprint
import time

options=Options()
options.add_argument('start-maximized')
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 30)

driver.get("https://www.rbc.ru/tags/?tag=%D0%AF%D0%BD%D0%B4%D0%B5%D0%BA%D1%81")
time.sleep(2)
button_one=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-filter-name='date']")))

button_one.click()
button_two=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-filter-value='30']")))
button_two.click()


cards = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[class='search-item js-search-item ']")))

count=len(cards)
print(count)

news=[]
for card in cards:
    event={}
    url = card.find_element(By.XPATH, "./div/a").get_attribute("href")
    ua = UserAgent().random
    header = {"User-Agent": ua}
    session = requests.session()

    response = session.get(url, headers=header, timeout=2)
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.find('h1', {'class', 'article__header__title-in js-slide-title'}).get_text(strip=True)
    time = soup.find('time', {'class', 'article__header__date'}).get_text(strip=True)
    contents = soup.findAll('p')
    final_content = []

    for content in contents:
        final_content.append(content.get_text(strip=True))

    event['title'] = title
    event['time'] = time
    event['content'] = final_content
    event['url'] = url
    news.append(event)

formatted_news=pd.DataFrame(news)
formatted_news.to_csv('news.csv')
formatted_news.to_json('news.json',orient='records', force_ascii=False, indent=4)
pprint(formatted_news)
