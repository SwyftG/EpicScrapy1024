# encoding: utf-8
__author__ = 'lianggao'
__date__ = '2018/5/11 下午3:47'

import urllib3
import random
from Epic1024.user_agents import agents

if __name__ == '__main__':
    file_root = "/Users/gaoliang/GaoGithub/EpicScrapy1024/Epic1024/Epic1024/output/"
    filename = file_root + "11" + ".torrent"
    url = "http://www.rmdown.com/download.php?reff=244396&ref=1824dc0fc5638214319fe73adf7498b55f3a2504ca1"
    http = urllib3.PoolManager()
    user_agent = random.choice(agents)
    headers = {"User-Agent": user_agent}
    response = http.request("GET", url, headers=headers)

    with open(filename, 'wb') as file:
        file.write(response.data)
    print(response.data)


