import scrapy
from scrapy.http import HtmlResponse
from Task_5.Task_5_in_home.openlibraryparser.openlibraryparser.items import OpenlibraryparserItem

class OpenlibraryorgSpider(scrapy.Spider):
    # Имя паука, используется для его запуска
    name = "openlibraryorg"
    # Домен, который паук может обрабатывать
    allowed_domains = ["openlibrary.org"]
    # Начальная страница для сканирования
    start_urls = ["https://openlibrary.org/trending/daily"]

    def parse(self, response: HtmlResponse):
        """
        Парсит начальную страницу (https://openlibrary.org/trending/daily)
        и извлекает ссылки на другие страницы с популярными книгами.
        """
        # Базовый URL для формирования полных ссылок
        base_url = "https://openlibrary.org"

        # Извлекаем ссылки на страницы
        page_half_links = response.xpath("//a[@class='ChoosePage']/@href").getall()

        if page_half_links:
            # Удаляем последний элемент ( ненужную ссылку)
            page_half_links.pop()
            # Формируем полные ссылки, добавляя base_url
            page_links = [base_url + s for s in page_half_links]
            # Добавляем текущую страницу
            page_links.append("https://openlibrary.org/trending/daily")
            # Проходимся по всем ссылкам и отправляем запросы
            for link in page_links:
                # Переходим по ссылке и вызываем метод `page_parse` для обработки
                yield response.follow(link, callback=self.page_parse)

    def page_parse(self, response: HtmlResponse):
        """
        Парсит страницы трендов (например, "ежедневные", "еженедельные")
        и извлекает ссылки на книги.
        """
        # Базовый URL для формирования полных ссылок на книги
        base_url = "https://openlibrary.org"

        # Извлекаем относительные ссылки на книги
        half_links = response.xpath("//span[@class='bookcover ']/a/@href").getall()

        # Формируем полные ссылки
        links = [base_url + s for s in half_links]

        # Проходимся по всем ссылкам на книги и отправляем запросы
        for link in links:
            # Переходим по ссылке и вызываем метод `books_parse` для обработки
            yield response.follow(link, callback=self.books_parse)

    def books_parse(self, response: HtmlResponse):
        """
        Парсит страницу книги и извлекает данные о книге (название, автор, описание, URL).
        """
        # Извлекаем название книги
        book_title = response.xpath("//h1[@class='work-title']/text()").get()
        # Извлекаем имя автора
        book_author = response.xpath("//a[@itemprop='author']/text()").get()
        # Извлекаем описание книги
        book_description = response.xpath("//div[@class='read-more__content']/p/text()").get()
        image_urls=['https:'+response.xpath("//img[@itemprop='image']/@src").get()]
        # Получаем URL текущей страницы
        book_url = response.url

        # Создаём объект OpenlibraryparserItem и передаём в него извлечённые данные
        yield OpenlibraryparserItem(
            book_title=book_title,
            book_author=book_author,
            book_description=book_description,
            image_urls=image_urls,
            book_url=book_url
        )
