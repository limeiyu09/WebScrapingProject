# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
    # define the fields for your item here like:
    
    brand = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    num_review = scrapy.Field()
    rating = scrapy.Field()
    sale_price = scrapy.Field()
    shoe_type = scrapy.Field()
