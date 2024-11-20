import scrapy
from scrapy.http import HtmlResponse
from pprint import pprint
from Task_5.Task_5_in_home.openlibraryparser.openlibraryparser.items import OpenlibraryparserItem

class OpenlibraryorgSpider(scrapy.Spider):
    name = "openlibraryorg"
    allowed_domains = ["openlibrary.org"]
    start_urls = ["https://openlibrary.org/trending/daily"]

    def parse(self, response: HtmlResponse):
        base_url = "https://openlibrary.org"
        page_half_links = response.xpath("//a[@class='ChoosePage']/@href").getall().pop()
        page_links = [base_url  + s for s in page_half_links]
        for link in page_links:
           yield response.follow(link, callback=self.page_parse)

    def page_parse(self, response: HtmlResponse):
        base_url = "https://openlibrary.org"
        half_links=response.xpath("//span[@class='bookcover']/a/@href").getall()
        links = [base_url +s for s in half_links]
        for link in links:
           yield response.follow(link, callback=self.books_parse)

    def books_parse(self, response: HtmlResponse):
        book_title = response.xpath("//h1[@class='work-title']/text()").get()
        book_author = response.xpath("//a[@itemprop='author']//text()").get()
        url = response.url
        yield OpenlibraryparserItem(name=name, salary=salary, url=url)