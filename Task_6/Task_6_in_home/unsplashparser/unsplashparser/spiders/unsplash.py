import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from Task_6.Task_6_in_home.unsplashparser.unsplashparser.items import UnsplashparserItem


class UnsplashSpider(scrapy.Spider):
    name = "unsplash"
    allowed_domains = ["unsplash.com"]
    start_urls = ["https://unsplash.com"]

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     self.start_urls = [self.start_urls]

    def closed(self, reason):
        self.crawler.stats.set_value("spider_name", self.name)

    def parse(self, response: HtmlResponse):
        links = response.xpath("//a[@class='wuIW2 R6ToQ']")[3:]
        for link in links:
            yield response.follow(link, callback=self.parse_book)

    def parse_image(self, response: HtmlResponse):
        # name = response.xpath("//h1/text()").get()
        # price = response.xpath("//span[@class='app-price product-sidebar-price__price']/text()").get()
        # url = response.url
        # photos = response.xpath("//picture[@class='product-poster__main-picture']/source[1]/@srcset | //picture[@class='product-poster__main-picture']/source[1]/@data-srcset").getall()
        # yield (BookparserItem(name=name, price=price, url=url, photos=photos))

        loader = ItemLoader(item=UnsplashparserItem(), response=response)
        loader.add_xpath(field_name='categories_name', xpath="//h1[@class='zbHmu L8kCG']/text()")
        loader.add_xpath(field_name='picture_name', xpath="//div[@class='wdUrX']/img[@alt]/@alt")
        loader.add_xpath(field_name='photos_urls', xpath="//div[@class='wdUrX']/img[@alt]/@src")
        loader.add_value(field_name='url', value=response.url)

        yield loader.load_item()