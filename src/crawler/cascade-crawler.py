import os
import json
import requests
from lxml import etree
import logging
import time

logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    json_file = open("data/hot.json",'r')
    json_content = json.load(json_file)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 Edg/86.0.622.51',
        "Cookie": "_T_WM=90755439678; SSOLoginState=1603853731; SCF=AtX3vPVu5ttzQ26RWfF1LqDZrPCAHdHbtxDtC8RTpumFGsYn2ACbXxp2N8vu0iKqpJwkbp94hRnKj9-97aG11q8.; SUB=_2A25ynK3zDeRhGeFK71IQ-CjKyjSIHXVufjO7rDV6PUJbktANLXXbkW1NQ3UP2YZtiluUmIy0uYIjOQaX1WWaCZT9; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5zFhy2Zvuj7.uSvTTHadc15JpX5KzhUgL.FoMXSh5p1hqceKn2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMNShB7SKeXe0n4; SUHB=0bts43emuDe7SW"
    }
    start_bid = "Ir50IkZCA"
    started = False
    skipped_count = 0
    for data in json_content:
        if(data["bid"] == start_bid):
            logging.info("skipped count: %d" % skipped_count)
            started = True
        if(not started):
            skipped_count += 1
            logging.info("skipped: %s" % data["bid"])
            continue
        bid = data["bid"]
        started = False
        last_gotten_length = 0
        page_count = 1
        if(not os.path.exists("data/cascade-html/%s"%bid)):
            os.mkdir("data/cascade-html/%s"%bid)
        page_size_delta = 0
        base_size = len(requests.get("https://weibo.cn/repost/" + "%s?page=%d" % (bid,400),headers = headers).content)
        while(True):
            if(started and (page_size_delta <= 5)):
                if(page_count < 30):
                    logging.info("page count is less than prefered. page_size_delta: %d" %page_size_delta)
                    time.sleep(60)
                print("breaking")
                break
            started = True
            page_content = requests.get("https://weibo.cn/repost/" + "%s?page=%d" % (bid,page_count),headers = headers).content
            page_size_delta = len(page_content) - base_size
            if(page_size_delta < -10):
                time.sleep(60)
                page_size_delta = 1000
                base_size = len(requests.get("https://weibo.cn/repost/%s?page=400" % bid,headers = headers).content)
                continue
            target_filename = "data/cascade-html/%s/%d.html" % (bid,page_count)
            target_file = open(target_filename,'wb')
            target_file.write(page_content)
            target_file.close()
            logging.info("target file: %s written." % target_filename)
            page_count += 1
            