# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy

def process_photo(value: str):
    return 'https:' + value


class OpenlibraryparserItem(scrapy.Item):
    """
    Класс для определения структуры элементов, которые собираются пауком.

    Каждый экземпляр этого класса представляет собой объект, содержащий данные о книге,
    которые извлекаются с сайта OpenLibrary.
    """
    # Название книги
    book_title = scrapy.Field()
    # Автор книги
    book_author = scrapy.Field()
    # Описание книги
    book_description = scrapy.Field()
    # URL страницы книги
    book_url = scrapy.Field()
    # Уникальный идентификатор для записи в MongoDB
    image_urls = scrapy.Field()
    _id = scrapy.Field()
