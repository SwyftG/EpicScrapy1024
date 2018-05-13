# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CLTopicItem(scrapy.Item):
    topic_id = scrapy.Field()
    topic_title = scrapy.Field()
    topic_image_url = scrapy.Field()
    topic_page_url = scrapy.Field()
    block_id = scrapy.Field()
    torrent_download_url = scrapy.Field()
    torrent_page_url = scrapy.Field()
