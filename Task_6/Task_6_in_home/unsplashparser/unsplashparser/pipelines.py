# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import scrapy
import hashlib
import csv
from pymongo import MongoClient
from scrapy import signals
from bson.json_util import dumps

class UnsplashparserPhotosPipeline(ImagesPipeline):
    def __init__(self):
        # Подключение к MongoDB
        try:
            client = MongoClient(host='localhost', port=27017)
            self.mongo_base = client.pictures  # Имя базы данных
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
        image_guid = hashlib.sha1(item['picture_name'].encode()).hexdigest()
        data['file_name']="photos$\$"+f"{item['picture_name']} - {image_guid}.jpg"

        # Проверяем, существует ли элемент с тем же `_id`
        if not collection.find_one({'_id': item.get('_id')}):
            collection.insert_one(data)  # Сохраняем элемент в MongoDB
        return item  # Обязательно возвращаем элемент для дальнейшей обработки Scrapy

    def spider_closed(self, spider):
        spider_name = spider.crawler.stats.get_value("spider_name")
        if not spider_name:
            raise ValueError("Spider name not found")

        collection = self.mongo_base[spider_name]
        all_data = list(collection.find())
        self.write_in_csv(all_data)

    def write_in_csv(self, data):
        """
        Сохраняет данные в файл формата CSV.
        :param data: список словарей с данными
        """
        filename = "unsplash.csv"
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

# class UnsplashparserPhotosPipeline(ImagesPipeline):
#     def file_path (self, request, response=None, info=None, *, item=None):
#         image_guid = hashlib.sha1(item['picture_name'].encode()).hexdigest()
#         return f"{item['name']} - {image_guid}.jpg"
