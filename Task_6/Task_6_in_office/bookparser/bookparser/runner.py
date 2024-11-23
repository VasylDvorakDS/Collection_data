from scrapy.crawler import CrawlerProcess
from scrapy.utils.reactor import install_reactor
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from Task_6.Task_6_in_office.bookparser.bookparser.spiders.book24 import Book24Spider

if __name__ == '__main__':
    install_reactor('twisted.internet.asyncioreactor.AsyncioSelectorReactor')
    configure_logging()
    process = CrawlerProcess(get_project_settings())
    # query = input('')
    process.crawl(Book24Spider, query='детектив')
    process.start()
