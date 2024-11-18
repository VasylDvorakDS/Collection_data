from lxml import html  # Для парсинга HTML-страниц с использованием XPath
import requests  # Для выполнения HTTP-запросов
from pprint import pprint  # Для красивого вывода данных
from pymongo import MongoClient  # Для работы с MongoDB
import csv  # Для записи данных в CSV-файл
from fake_useragent import UserAgent  # Для генерации случайных User-Agent


# Функция для сохранения данных в MongoDB
def save_data_to_mongo(data):
    """
    Сохраняет данные в базу данных MongoDB.
    :param data: список словарей с данными рецептов
    """
    client = MongoClient('localhost', 27017)  # Подключение к MongoDB на локальном хосте
    db = client['cookingclassy']  # Создание/выбор базы данных
    collection = db['recipes_meat']  # Создание/выбор коллекции
    collection.insert_many(data)  # Массовая вставка данных


# Функция для записи данных в CSV-файл
def write_in_csv(data):
    """
    Сохраняет данные в файл формата CSV.
    :param data: список словарей с данными рецептов
    """
    filename = "receipts.csv"  # Имя выходного файла
    headers = data[0].keys()  # Используем ключи первого словаря как заголовки CSV
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers)  # Объект для записи словарей в CSV
        writer.writeheader()  # Записываем заголовки
        writer.writerows(data)  # Записываем строки
    print(f"Данные успешно записаны в файл {filename}.")


# Создаём объект UserAgent для случайного выбора User-Agent
ua = UserAgent()
header = {'User-Agent': ua.random}  # Формируем заголовок с случайным User-Agent

# URL для сбора данных
url = 'https://www.cookingclassy.com/recipes/meat/'

# Выполняем GET-запрос на указанную страницу
response = requests.get(url, headers=header)
dom = html.fromstring(response.text)  # Преобразуем HTML-код страницы в DOM-объект

# Извлекаем ссылки на страницы рецептов
links = dom.xpath("//div[@class='li-a']/a/@href")  # Используем XPath для поиска всех ссылок

# Список для хранения данных о рецептах
receipts_list = []

# Обрабатываем каждую ссылку
for link in links:
    receipt_info = {}  # Словарь для хранения данных о текущем рецепте

    # Обновляем User-Agent для каждого запроса
    header = {'User-Agent': ua.random}

    # Загружаем страницу рецепта
    page = html.fromstring(requests.get(link, headers=header).text)

    # Извлекаем заголовок рецепта
    receipt_info['title'] = page.xpath("//h1[@class='title']/text()")[0]

    # Извлекаем ингредиенты из группы ингредиентов
    list_ingredients = page.xpath("//div[@class='wprm-recipe-ingredient-group'][1]/ul/li")
    ingredients = []  # Список для хранения ингредиентов
    for ingr in list_ingredients:
        ingred = ingr.xpath("./span/text()")  # Извлекаем текстовые данные каждого ингредиента
        one_ingredient = ""  # Строка для хранения одного ингредиента
        for ing in ingred:
            one_ingredient += ing + " "  # Объединяем части ингредиента в одну строку
        ingredients.append(one_ingredient.strip())  # Убираем лишние пробелы и добавляем в список

    receipt_info['ingredients'] = ingredients  # Сохраняем список ингредиентов

    # Извлекаем инструкции по приготовлению
    receipt_info['instruction'] = page.xpath("//div[@class='wprm-recipe-instruction-group']/ul/li/div/span/text()")

    # Извлекаем список ингредиентов для подачи
    receipt_info['list_for_serving'] = page.xpath("//div[@class='wprm-recipe-ingredient-group'][2]/ul/li/span/text()")

    # Добавляем данные о рецепте в общий список
    receipts_list.append(receipt_info)

# Сохраняем данные в MongoDB
save_data_to_mongo(receipts_list)

# Сохраняем данные в CSV
write_in_csv(receipts_list)

# Выводим данные в удобном формате
pprint(receipts_list)
