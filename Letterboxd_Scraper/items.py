# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LetterboxdScraperItem(scrapy.Item):
    title = scrapy.Field()
    year = scrapy.Field()
    director = scrapy.Field()
    running_time = scrapy.Field()
    views = scrapy.Field()
    likes = scrapy.Field()
    avg_rating = scrapy.Field()
    half_star = scrapy.Field()
    one_star = scrapy.Field()
    one_half_star = scrapy.Field()
    two_star = scrapy.Field()
    two_half_star = scrapy.Field()
    three_star = scrapy.Field()
    three_half_star = scrapy.Field()
    four_star = scrapy.Field()
    four_half_star = scrapy.Field()
    five_star = scrapy.Field()
