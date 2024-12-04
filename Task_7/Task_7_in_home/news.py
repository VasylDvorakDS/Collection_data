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

# Функция для настройки драйвера Selenium
def setup_driver():
    options = Options()  # Создаем объект настроек браузера
    options.add_argument('start-maximized')  # Устанавливаем запуск браузера в полноэкранном режиме
    return webdriver.Chrome(options=options)  # Возвращаем настроенный драйвер Chrome

# Функция для получения ссылок на статьи с сайта
def fetch_article_links(driver, wait):
    # Переходим на страницу с новостями по тегу "Яндекс"
    driver.get("https://www.rbc.ru/tags/?tag=%D0%AF%D0%BD%D0%B4%D0%B5%D0%BA%D1%81")
    # Ждем появления и кликаем на фильтр "За всё время"
    wait.until(EC.presence_of_element_located((By.XPATH, "//div[@data-filter-name='date']"))).click()
    # Ждем появления и кликаем на фильтр "За месяц"
    wait.until(EC.presence_of_element_located((By.XPATH, "//a[@data-filter-value='30']"))).click()
    # Ждём карточки новостей за месяц
    cards = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a[@class='search-item__link  js-search-item-link']")))
    # Собираем ссылки на статьи
    return [card.get_attribute("href") for card in cards]

# Функция для получения данных статьи с помощью Beatuful soup
def fetch_article_data(url):
    ua = UserAgent().random  # Создаем случайный User-Agent
    header = {"User-Agent": ua}  # Устанавливаем User-Agent в заголовки запроса
    try:
        response = requests.get(url, headers=header, timeout=10)  # Делаем запрос на страницу статьи
        soup = BeautifulSoup(response.text, "html.parser")  # Парсим HTML-страницу
        # Извлекаем заголовок статьи
        title = soup.find('h1', {'class', 'article__header__title-in js-slide-title'}).get_text(strip=True)
        # Извлекаем дату публикации
        time = soup.find('time', {'class', 'article__header__date'}).get_text(strip=True)
        # Извлекаем текст статьи
        content = [p.get_text(strip=True) for p in soup.findAll('p')]
        try:
            cut_index=content.index("Читайте РБК вTelegram.")
            content=content[:cut_index]
        except:
            pass
        article = '\n'.join(content)
        # Возвращаем данные статьи в виде словаря
        return {'title': title, 'time': time, 'content': article, 'url': url}
    except Exception as e:  # Обрабатываем возможные ошибки
        print(f"Ошибка обработки статьи {url}: {e}")  # Выводим сообщение об ошибке
        return None  # Возвращаем None в случае ошибки

# Основная программа

driver = setup_driver()  # Настраиваем и запускаем драйвер
wait = WebDriverWait(driver, 30)  # Устанавливаем ожидание до 30 секунд

try:
    # Получаем ссылки на статьи
    article_links = fetch_article_links(driver, wait)
    # По каждой ссылке извлекаем данные
    news = [fetch_article_data(url) for url in article_links if url]
    # Удаляем пустые результаты (где данные не были получены)
    news = [item for item in news if item]

    # Сохраняем данные в файлы
    formatted_news = pd.DataFrame(news)  # Преобразуем данные в таблицу
    formatted_news.to_csv('news.csv', index=False)  # Сохраняем данные в CSV-файл
    formatted_news.to_json('news.json', orient='records', force_ascii=False, indent=4)  # Сохраняем данные в JSON-файл
    pprint(news)  # Выводим данные в консоль
finally:
    driver.quit()  # Закрываем браузер, чтобы освободить ресурсы


