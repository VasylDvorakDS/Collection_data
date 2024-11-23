# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Compose



def process_name(value):
    value = value[0].strip()
    return value

def process_price(value):
    value = value[0].strip().replace('\xa0', ' ').split()
    if value[0].isdigit():
        value[0] = int(value[0])
    return value

def process_photo(value: str):
    first_split=value.split(',')[-1]
    second_split=first_split.split()[0]
    return second_split


class UnsplashparserItem(scrapy.Item):
    categories_name = scrapy.Field(input_processor=TakeFirst())
    picture_name = scrapy.Field(input_processor=TakeFirst())
    photos_urls = scrapy.Field(input_processor=TakeFirst())
    url = scrapy.Field(input_processor=TakeFirst())
    _id = scrapy.Field()
