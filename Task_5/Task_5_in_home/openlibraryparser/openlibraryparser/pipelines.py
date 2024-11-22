# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv
from itemadapter import ItemAdapter
from pymongo import MongoClient
from scrapy import signals
from bson.json_util import dumps


class OpenlibraryparserPipeline:
    def __init__(self):
        # Подключение к MongoDB
        try:
            client = MongoClient(host='localhost', port=27017)
            self.mongo_base = client.bookslibrary  # Имя базы данных
        except Exception as e:
            print(f"Failed to connect to MongoDB: {e}")
        self.collection_name = None  # Инициализация имени коллекции пока неизвестно имена коллекций от пауков

    @classmethod
    def from_crawler(cls, crawler):
        """
        Подключение сигнала `spider_closed` к пайплайну.
        Этот метод вызывается Scrapy при инициализации пайплайна.
        """
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_closed, signal=signals.spider_closed)
        return pipeline

    def process_item(self, item, spider):
        """
        Обработка каждого элемента, собранного пауком.
        :param item: Элемент (объект Item или словарь)
        :param spider: Объект паука
        """
        if not self.collection_name:
            self.collection_name = spider.name  # Установка имени коллекции в MongoDB на основе имени паука
        collection = self.mongo_base[self.collection_name]
        data = ItemAdapter(item).asdict()  # Преобразование элемента в словарь

        # Проверяем, существует ли элемент с тем же `_id`
        if not collection.find_one({'_id': item.get('_id')}):
            collection.insert_one(data)  # Сохраняем элемент в MongoDB
        return item  # Обязательно возвращаем элемент для дальнейшей обработки Scrapy

    def spider_closed(self, spider):
        """
        Обработчик сигнала `spider_closed`, вызывается при завершении работы паука.
        Этот метод отвечает за экспорт данных из MongoDB в файлы.
        """
        collection = self.mongo_base[self.collection_name]
        all_data = list(collection.find())  # Извлекаем все данные из коллекции MongoDB
        self.write_in_csv(all_data)  # Записываем данные в CSV
        self.write_in_json(all_data)  # Записываем данные в JSON

    def write_in_csv(self, data):
        """
        Сохраняет данные в файл формата CSV.
        :param data: список словарей с данными
        """
        filename = "openlibraryorg.csv"
        if not data:  # Проверяем, что данные не пустые
            print("Нет данных для записи в CSV.")
            return
        headers = list(data[0].keys())  # Используем ключи первого словаря как заголовки CSV
        try:
            with open(filename, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=headers)
                writer.writeheader()  # Записываем заголовки
                writer.writerows(data)  # Записываем строки
                print(f"Данные успешно записаны в файл {filename}.")
        except Exception as e:
            print("Ошибка записи в CSV файл:", e)

    def write_in_json(self, data):
        """
        Сохраняет данные в файл формата JSON.
        :param data: список словарей с данными
        """
        filename = "openlibraryorg.json"
        try:
            # Преобразуем данные в строку JSON
            json_data = dumps(data, indent=4, ensure_ascii=False)

            # Записываем строку JSON в файл
            with open(filename, "w", encoding="utf-8") as json_file:
                json_file.write(json_data)

            print(f"Данные успешно записаны в файл {filename}.")
        except Exception as e:
            print("Ошибка записи в JSON файл:", e)