# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import pymongo
import random
import requests
from Epic1024.user_agents import agents
from Epic1024.items import CLTopicItem
from Epic1024.settings import LOCAL_FILE_ROOT


class Epic1024Pipeline(object):
    def __init__(self):
        clinet = pymongo.MongoClient("localhost", 27017)
        db = clinet["Epic1024"]
        self.fib15 = db["fid15"]
        self.fib2 = db["fid2"]
        self.fib4 = db["fid4"]
        self.fib25 = db["fid25"]
        self.fib26 = db["fid26"]

    def process_item(self, item, spider):
        # 结果写入文件
        file_root = LOCAL_FILE_ROOT
        filename = file_root + item['block_id'] + ".txt"
        result_root_file = open(filename, 'a')
        result_root_file.write(item['block_id'] + ",")
        result_root_file.write(item['topic_id'] + ",")
        result_root_file.write(item['topic_title'] + ",")
        result_root_file.write(item['topic_page_url'] + ",")
        result_root_file.write(item['torrent_page_url'] + ",")
        img_str = "["
        for i in range(len(item['topic_image_url'])):
            img = item['topic_image_url'][i]
            if i == len(item['topic_image_url']) - 1:
                img_str = img_str + img
            else:
                img_str = img_str + img + ", "
        img_str = img_str + "]"
        result_root_file.write(img_str + ",\n")
        result_root_file.close()
        # 保存到数据库中
        if isinstance(item, CLTopicItem):
            try:
                if item['block_id'] == "15":
                    self.fib15.insert(dict(item))
                elif item['block_id'] == "2":
                    self.fib2.insert(dict(item))
                elif item['block_id'] == "4":
                    self.fib4.insert(dict(item))
                elif item['block_id'] == "25":
                    self.fib25.insert(dict(item))
                elif item['block_id'] == "26":
                    self.fib26.insert(dict(item))
                else:
                    print("!!!!!!!")
            except Exception as e:
                logging.error("PIPLINE EXCEPTION: " + str(e))
        return item