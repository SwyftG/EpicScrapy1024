# -*- coding: utf-8 -*-
import scrapy
import logging
import re
import random
import requests
import traceback
from scrapy.selector import Selector
from scrapy.spider import CrawlSpider
from scrapy import Request
from bs4 import BeautifulSoup
from Epic1024.blockid import BLOCK_ID
from Epic1024.items import CLTopicItem
from Epic1024.user_agents import agents
from Epic1024.settings import LOCAL_FILE_ROOT, ROOT_URL, CRAW_MAX_PAGES


class CaoliuSpider(CrawlSpider):
    name = 'Epic1024Spider'
    root_url = ROOT_URL
    local_file_root = LOCAL_FILE_ROOT
    max_page = CRAW_MAX_PAGES
    logging.getLogger("requests").setLevel(logging.WARNING)  # 将requests的日志级别设成WARNING
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='cataline.log',
                        filemode='w')

    def start_requests(self):
        for id in BLOCK_ID:
            request_url = self.root_url + "thread0806.php?fid=" + id + "&search=&page=1"
            yield Request(url=request_url, callback=self.parse_block_page)

    def parse_block_page(self, response):
        response_url_list = response.url.split('/')
        root_url = response_url_list[0] + "//" + response_url_list[2] + "/"
        page_num = response_url_list[-1].split('=')[-1]
        block_id = response_url_list[-1].split('=')[-3].split('&')[0]
        content = response.body
        soup = BeautifulSoup(content, "html.parser")
        temp_list = soup.find_all('a', attrs={'href': True, 'id': True})
        for item in temp_list:
            if "htm" not in item['href']:
                continue
            topic_id = item['href'].split('/')[3].split('.')[0]
            if len(topic_id) < 6:
                continue
            topic_url = root_url + item['href']
            yield Request(url=topic_url, callback=self.parse_info_page,
                          meta={'page_num': page_num, 'page_id': topic_id, 'block_id': block_id})
        next_page_num = int(page_num) + 1
        next_page_url = response.url[:-len(page_num)] + str(next_page_num)
        if next_page_num < self.max_page:
            yield Request(url=next_page_url, callback=self.parse_block_page)

    def parse_info_page(self, response):
        content = response.body
        soup = BeautifulSoup(content, "html.parser")
        block_id = response.meta['block_id']
        topic_url = response.url
        topic_id = response.meta['page_id']
        title_list = soup.find_all('h4')
        topic_title = title_list[0].text
        img_list = soup.find_all('img')
        topic_img_list = list()
        image_count = 0
        for item in img_list:
            if 'gif' in item['src']:
                continue
            if image_count < 4:
                topic_img_list.append(item['src'])
                image_count = image_count + 1
            else:
                break

        a_list = soup.find_all('a')
        topic_torrent_url = ""
        for item in a_list:
            if "rmdown" in item.text:
                topic_torrent_url = item.text
        if topic_torrent_url != "":
            yield Request(url=topic_torrent_url, callback=self.parse_torrent_page,
                          meta={'topic_url': topic_url, 'topic_title': topic_title, 'topic_id': topic_id,
                                'topic_img_list': topic_img_list, 'block_id': block_id})

    def parse_torrent_page(self, response):
        content = response.body
        soup = BeautifulSoup(content, "html.parser")
        topic_url = response.meta['topic_url']
        topic_title = response.meta['topic_title']
        topic_id = response.meta['topic_id']
        topic_img_list = response.meta['topic_img_list']
        topic_torrent_url = response.url
        block_id = response.meta['block_id']

        reff_value = soup.findAll(attrs={'name': 'reff'})
        ref_value = soup.findAll(attrs={'name': 'ref'})

        torrent_download_url = topic_torrent_url.split('?')[0].replace('link', 'download') + "?reff=" + reff_value[0][
            'value'] + "&ref=" + ref_value[0]['value']

        item = CLTopicItem()
        item['topic_id'] = topic_id
        item['topic_title'] = topic_title
        item['topic_image_url'] = topic_img_list
        item['topic_page_url'] = topic_url
        item['block_id'] = block_id
        item['torrent_download_url'] = torrent_download_url
        item['torrent_page_url'] = topic_torrent_url
        # 对种子名字做处理，使之合理可用
        longest_str = ""
        temp_list = topic_title.split("]")
        for s in temp_list:
            if len(s) > len(longest_str):
                longest_str = s
        torrent_name = longest_str.split("[")[0].strip()
        logging.debug("torrent name: " + torrent_name)
        # donwload种子文件
        file_root = self.local_file_root + block_id + "/"
        filename = file_root + torrent_name + ".torrent"
        try:
            user_agent = random.choice(agents)
            headers = {"User-Agent": user_agent}
            response = requests.get(torrent_download_url, headers=headers)
            logging.debug("response code: " + str(response.status_code))
            if response.status_code == 200:
                with open(filename, 'xb') as file:
                    file.write(response.content)
        except Exception as e:
            ext = traceback.format_exc()
            logging.error("ECXEPTION: topoc_id: " + topic_id + "\n" + ext)
        # print("********************")
        # print(topic_url)
        # print(topic_title)
        # print(topic_id)
        # print(topic_img_list)
        # print(topic_torrent_url)
        # print(torrent_download_url)
        # print(block_id)
        yield item
