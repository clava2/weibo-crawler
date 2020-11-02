import os
import json
import requests
from lxml import etree

if __name__ == "__main__":
    dirs = os.listdir("data/final_jsons")
    dirs.sort()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 Edg/86.0.622.51',
        "Cookie": "_T_WM=90755439678; SSOLoginState=1603853731; SCF=AtX3vPVu5ttzQ26RWfF1LqDZrPCAHdHbtxDtC8RTpumFGsYn2ACbXxp2N8vu0iKqpJwkbp94hRnKj9-97aG11q8.; SUB=_2A25ynK3zDeRhGeFK71IQ-CjKyjSIHXVufjO7rDV6PUJbktANLXXbkW1NQ3UP2YZtiluUmIy0uYIjOQaX1WWaCZT9; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5zFhy2Zvuj7.uSvTTHadc15JpX5KzhUgL.FoMXSh5p1hqceKn2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMNShB7SKeXe0n4; SUHB=0bts43emuDe7SW"
    }
    for dir in dirs:
        print(dir)
        json_content = json.load(open("data/final_jsons/" + dir))
        # print(json_content)
        processed = {}
        started = False
        last_gotten_length = 0
        page_count = 1
        while(True):
            if(started and (last_gotten_length == 0)):
                print("breaking")
                break
            started = True
            page_content = requests.get("https://weibo.cn/repost/" + "IozThgAp3?page=%d" % page_count,headers = headers).content
            parse_result = etree.HTML(page_content)
            user_ids = list([t.attrib["href"].split("/")[-1] for t in parse_result.xpath('/html/body/div[@class="c"]/a[1]')])
            retweet_time = list([t.text.split("\xa0")[1] for t in parse_result.xpath('/html/body/div[@class="c"]/span[@class="ct"]')])
            last_gotten_length = len(user_ids)
            if(len(user_ids) != len(retweet_time)):
                print("length is not the same")
            print("processing %s, page: %d, gotten length: %d" % (dir,page_count,last_gotten_length))
            processed.update({user_ids[i]: retweet_time[i] for i in range(last_gotten_length)})
            page_count += 1
        print(len(processed))