# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field

class RmdailyItem(scrapy.Item):
	title = Field()
	url = Field()
	author = Field()
	date = Field()
	content = Field()
