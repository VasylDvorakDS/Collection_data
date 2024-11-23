from fake_useragent import UserAgent
from scrapy.crawler import CrawlerProcess
from scrapy.utils.reactor import install_reactor
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from Task_6.Task_6_in_home.unsplashparser.unsplashparser.spiders.unsplash import UnsplashSpider
from Task_6.Task_6_in_office.bookparser.bookparser.spiders.book24 import Book24Spider
import requests
if __name__ == '__main__':

    #install_reactor('twisted.internet.asyncioreactor.AsyncioSelectorReactor')
    configure_logging()
    process = CrawlerProcess(get_project_settings())
    #query = input('Введите категорию картинок запроса: ')
    process.crawl(UnsplashSpider)



    process.start()
