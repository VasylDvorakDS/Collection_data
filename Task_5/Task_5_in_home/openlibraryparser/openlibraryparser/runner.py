from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from Task_5.Task_5_in_home.openlibraryparser.openlibraryparser.spiders.openlibraryorg import OpenlibraryorgSpider

if __name__ == '__main__':
    """
    Этот блок выполняется только при прямом запуске файла.
    Используется для запуска паука OpenlibraryorgSpider через скрипт Python.
    """
    # Настраиваем систему логирования Scrapy
    configure_logging()
    # Создаём объект CrawlerProcess для управления пауками
    process = CrawlerProcess(get_project_settings())
    # Добавляем паука OpenlibraryorgSpider в процесс
    process.crawl(OpenlibraryorgSpider)
    # Запускаем выполнение паука (блокирующий вызов)
    process.start()
